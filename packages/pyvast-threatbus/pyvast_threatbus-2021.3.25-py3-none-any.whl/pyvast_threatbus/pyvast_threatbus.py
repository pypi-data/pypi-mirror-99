#!/usr/bin/env python3

import argparse
import asyncio
import atexit
import coloredlogs
import confuse
import json
import logging
from .message_mapping import (
    get_vast_type_and_value,
    indicator_to_vast_matcher_ioc,
    indicator_to_vast_query,
    matcher_result_to_sighting,
    query_result_to_sighting,
    split_object_path_and_value,
)
from pyvast import VAST
import random
from shlex import split as lexical_split
import socket
from string import ascii_lowercase as letters
import sys
from .metrics import Gauge, Summary
from stix2 import parse, Indicator, Sighting
from threatbus.logger import setup as setup_logging_threatbus
from threatbus.data import Operation, ThreatBusSTIX2Constants

import time
import zmq

logger_name = "pyvast-threatbus"
logger = logging.getLogger(logger_name)
matcher_name = None
# list of all running async tasks of the bridge
async_tasks = []
# the p2p topic that was given to the vast-bridge upon successful subscription
p2p_topic = None
max_open_tasks = None

# metric definitions
metrics = []
g_iocs_added = Gauge("added_iocs")
g_iocs_removed = Gauge("removed_iocs")
metrics += [g_iocs_added, g_iocs_removed]
s_retro_matches_per_ioc = Summary("retro_matches_per_ioc")
s_retro_query_time_s_per_ioc = Summary("retro_query_time_per_ioc")
g_live_matcher_sightings = Gauge("live_matcher_sightings")


def setup_logging_with_level(level: str):
    """
    Sets up a the global logger for console logging with the given loglevel.
    @param level The loglevel to use, e.g., "DEBUG"
    """
    global logger
    log_level = logging.getLevelName(level.upper())

    fmt = "%(asctime)s %(levelname)-8s %(message)s"
    colored_formatter = coloredlogs.ColoredFormatter(fmt)

    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    if logger.level > log_level or logger.level == 0:
        logger.setLevel(log_level)
    handler.setFormatter(colored_formatter)
    logger.addHandler(handler)


def setup_logging_with_config(config: confuse.Subview):
    """
    Sets up the global logger as configured in the `config` object.
    @param config The user-defined logging configuration
    """
    global logger
    logger = setup_logging_threatbus(config, logger_name)


def validate_config(config: confuse.Subview):
    assert config, "config must not be None"
    config["vast"].get(str)
    config["vast_binary"].get(str)
    config["threatbus"].get(str)
    config["snapshot"].get(int)
    live_match = config["live_match"].get(bool)
    retro_match = config["retro_match"].get(bool)
    assert (
        live_match or retro_match
    ), "please enable at least one kind of matching (live_match and/or retro_match)"
    config["retro_match_max_events"].get(int)
    config["max_background_tasks"].get(int)

    # fallback values for the optional arguments
    config["transform_context"].add(None)
    config["sink"].add(None)

    # logging
    if config["logging"]["console"].get(bool):
        config["logging"]["console_verbosity"].get(str)
    if config["logging"]["file"].get(bool):
        config["logging"]["file_verbosity"].get(str)
        config["logging"]["filename"].get(str)

    # metrics
    config["metrics"]["interval"].get(int)
    config["metrics"]["filename"].get(str)


def cancel_async_tasks():
    """
    Cancels all async tasks.
    """
    global async_tasks
    for task in async_tasks:
        task.cancel()
        del task
    async_tasks = []


async def start(
    vast_binary: str,
    vast_endpoint: str,
    zmq_endpoint: str,
    snapshot: int,
    live_match: bool,
    retro_match: bool,
    retro_match_max_events: int,
    max_open_files: int,
    metrics_interval: int,
    metrics_filename: str,
    transform_cmd: str = None,
    sink: str = None,
):
    """
    Starts the app between the two given endpoints. Subscribes the configured
    VAST instance for threat intelligence (IoCs) and reports new sightings to
    Threat Bus.
    @param cmd The vast binary command to use with PyVAST
    @param vast_endpoint The endpoint of a running VAST node ('host:port')
    @param zmq_endpoint The ZMQ management endpoint of Threat Bus ('host:port')
    @param snapshot An integer value to request n days of historical IoC items
    @param live_match Boolean flag to enable live-matching
    @param retro_match Boolean flag to enable retro-matching
    @param retro_match_max_events Max amount of retro match results
    @param max_open_files The maximum number of concurrent background tasks for VAST queries.
    @param merics_interval The interval in seconds to bucketize metrics
    @param metrics_filename The filename (system path) to store metrics at
    @param transform_cmd The command to use to transform Sighting context with
    @param sink Forward sighting context to this sink (subprocess) instead of
        reporting back to Threat Bus
    """
    global logger, async_tasks, p2p_topic, max_open_tasks, metrics
    # needs to be created inside the same eventloop where it is used
    max_open_tasks = asyncio.Semaphore(max_open_files)
    vast = VAST(binary=vast_binary, endpoint=vast_endpoint, logger=logger)
    assert await vast.test_connection() is True, "Cannot connect to VAST"

    logger.debug(f"Calling Threat Bus management endpoint {zmq_endpoint}")
    reply = subscribe(zmq_endpoint, "stix2/indicator", snapshot)
    if not reply_is_success(reply):
        logger.error("Subscription failed")
        return
    pub_endpoint = reply.get("pub_endpoint", None)
    sub_endpoint = reply.get("sub_endpoint", None)
    topic = reply.get("topic", None)
    if not pub_endpoint or not sub_endpoint or not topic:
        logger.error("Subscription failed")
        return
    logger.info(f"Subscription successful. New p2p_topic: {topic}")
    if p2p_topic:
        # The 'start' function is called as result of a restart
        # Unsubscribe the old topic as soon as we get a working connection
        logger.info("Cleaning up old p2p_topic subscription ...")
        unsubscribe(zmq_endpoint, p2p_topic)
        atexit.unregister(unsubscribe)
    p2p_topic = topic
    atexit.register(unsubscribe, zmq_endpoint, topic)

    async_tasks.append(
        asyncio.create_task(heartbeat(zmq_endpoint, p2p_topic, interval=5))
    )

    indicator_queue = asyncio.Queue()
    sightings_queue = asyncio.Queue()
    async_tasks.append(
        asyncio.create_task(
            report_sightings(sub_endpoint, sightings_queue, transform_cmd, sink)
        )
    )

    async_tasks.append(
        asyncio.create_task(receive(pub_endpoint, p2p_topic, indicator_queue))
    )

    async_tasks.append(
        asyncio.create_task(
            match_intel(
                vast_binary,
                vast_endpoint,
                indicator_queue,
                sightings_queue,
                live_match,
                retro_match,
                retro_match_max_events,
            )
        )
    )

    if retro_match:
        # add metrics for retro-matching to the metric output
        metrics += [s_retro_matches_per_ioc, s_retro_query_time_s_per_ioc]
    if live_match:
        # add metrics for live-matching to the metric output
        metrics.append(g_live_matcher_sightings)
        async_tasks.append(
            asyncio.create_task(
                live_match_vast(vast_binary, vast_endpoint, sightings_queue)
            )
        )

    if metrics_interval:
        async_tasks.append(
            asyncio.create_task(write_metrics(metrics_interval, metrics_filename))
        )

    atexit.register(cancel_async_tasks)
    return await asyncio.gather(*async_tasks)


async def write_metrics(every: int, to: str):
    """
    Periodically writes metrics to a file.
    @param every The interval to write metrics, in seconds
    @param to the filepath to write to
    """
    while True:
        line = f"pyvast-threatbus,host={socket.gethostname()}"
        start_length = len(line)
        for m in metrics:
            if not m.is_set:
                continue
            if type(m) is Gauge:
                line += f" {m.name}={m.value}"
            if type(m) is Summary:
                line += (
                    f" {m.name}_min={m.min},{m.name}_max={m.max},{m.name}_avg={m.avg}"
                )
            m.reset()

        if len(line) > start_length:
            # only update the file if there were metrics collected.
            line += f" {time.time_ns()}"  # append current nanoseconds ts
            with open(to, "a") as f:
                f.write(line + "\n")

        await asyncio.sleep(every)


async def receive(pub_endpoint: str, topic: str, indicator_queue: asyncio.Queue):
    """
    Starts a zmq subscriber on the given endpoint and listens for new messages
    that are published on the given topic (zmq prefix matching). Depending on
    the topic suffix, Indicators are enqueued to the indicator_queue.
    @param pub_endpoint A host:port string to connect to via zmq
    @param topic The topic prefix to subscribe to intelligence items
    @param indicator_queue The queue to put arriving IoCs into
    """
    global logger
    socket = zmq.Context().socket(zmq.SUB)
    socket.connect(f"tcp://{pub_endpoint}")
    socket.setsockopt(zmq.SUBSCRIBE, topic.encode())
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    logger.info(f"Receiving via ZMQ on topic {pub_endpoint}/{topic}")
    while True:
        socks = dict(
            poller.poll(timeout=100)
        )  # note that smaller timeouts may increase CPU load
        if socket in socks and socks[socket] == zmq.POLLIN:
            try:
                topic, msg = socket.recv().decode().split(" ", 1)
            except Exception as e:
                logger.error(f"Error decoding message: {e}")
                continue
            # the topic is suffixed with the message type
            if not topic.endswith("indicator"):
                # pyvast-threatbus is not (yet) interested in Sightings or SnapshotRequests
                logger.debug(f"Skipping unsupported message: {msg}")
                continue
            await indicator_queue.put(msg)
        else:
            await asyncio.sleep(0.05)  # free event loop for other tasks


async def retro_match_vast(
    vast_binary,
    vast_endpoint,
    retro_match_max_events,
    indicator,
    sightings_queue,
):
    """
    Turns the given STIX-2 Indicator into a valid VAST query and forwards all
    query results (sightings) to the sightings_queue.
    @param vast_binary The vast binary command to use with PyVAST
    @param vast_endpoint The endpoint of a running vast node ('host:port')
    @param retro_match_max_events  Max amount of retro match results
    @param indicator The STIX-2 Indicator to query VAST for
    @param sightings_queue The queue to put new sightings into
    """
    start = time.time()
    query = indicator_to_vast_query(indicator)
    if not query:
        return
    global logger, max_open_tasks
    async with max_open_tasks:
        vast = VAST(binary=vast_binary, endpoint=vast_endpoint, logger=logger)
        kwargs = {}
        if retro_match_max_events > 0:
            kwargs["max_events"] = retro_match_max_events
        proc = await vast.export(**kwargs).json(query).exec()
        reported = 0
        while not proc.stdout.at_eof():
            line = (await proc.stdout.readline()).decode().rstrip()
            if line:
                sighting = query_result_to_sighting(line, indicator)
                if not sighting:
                    logger.error(f"Could not parse VAST query result: {line}")
                    continue
                reported += 1
                await sightings_queue.put(sighting)
        logger.debug(f"Retro-matched {reported} sighting(s) for indicator: {indicator}")
        s_retro_matches_per_ioc.observe(reported)
        s_retro_query_time_s_per_ioc.observe(time.time() - start)


async def ingest_vast_ioc(vast_binary: str, vast_endpoint: str, indicator: Indicator):
    """
    Converts the given STIX-2 Indicator to a VAST-compatible IoC and ingests it
    via a VAST matcher.
    @param vast_binary The vast binary command to use with PyVAST
    @param vast_endpoint The endpoint of a running vast node ('host:port')
    @param indicator The STIX-2 Indicator to query VAST for
    """
    global logger
    vast_ioc = indicator_to_vast_matcher_ioc(indicator)
    if not vast_ioc:
        logger.error(
            f"Unable to convert STIX-2 Indicator to VAST compatible IoC. Is it a point IoC? {indicator}"
        )
        return
    vast = VAST(binary=vast_binary, endpoint=vast_endpoint, logger=logger)
    proc = await vast.import_().json(type="intel.indicator").exec(stdin=vast_ioc)
    await proc.wait()
    logger.debug(f"Ingested indicator for VAST live matching: {indicator}")


async def remove_vast_ioc(vast_binary: str, vast_endpoint: str, indicator: Indicator):
    """
    Converts the given STIX-2 Indicator to a VAST-compatible IoC and removes it
    from the VAST matcher.
    @param vast_binary The vast binary command to use with PyVAST
    @param vast_endpoint The endpoint of a running vast node ('host:port')
    @param indicator The STIX-2 Indicator to remove from VAST
    """
    global logger, matcher_name
    type_and_value = get_vast_type_and_value(indicator.pattern)
    if not type_and_value:
        logger.debug(f"Cannot remove IoC from VAST. Is it a point IoC? {indicator}")
        return None
    (vast_type, ioc_value) = type_and_value
    vast = VAST(binary=vast_binary, endpoint=vast_endpoint, logger=logger)
    await vast.matcher().ioc_remove(matcher_name, ioc_value, vast_type).exec()
    logger.debug(f"Removed indicator from VAST live matching: {indicator}")


async def match_intel(
    vast_binary: str,
    vast_endpoint: str,
    indicator_queue: asyncio.Queue,
    sightings_queue: asyncio.Queue,
    live_match: bool,
    retro_match: bool,
    retro_match_max_events: int,
):
    """
    Reads from the indicator_queue and matches all IoCs, either via VAST's
    live-matching or retro-matching.
    @param vast_binary The vast binary command to use with PyVAST
    @param vast_endpoint The endpoint of a running vast node ('host:port')
    @param indicator_queue The queue to read new IoCs from
    @param sightings_queue The queue to put new sightings into
    @param live_match Boolean flag to use retro-matching
    @param retro_match Boolean flag to use live-matching
    @param retro_match_max_events  Max amount of retro match results
    """
    global logger, open_tasks
    while True:
        msg = await indicator_queue.get()
        try:
            indicator = parse(msg, allow_custom=True)
        except Exception as e:
            logger.warning(f"Failed to decode STIX-2 Indicator item {msg}: {e}")
            continue
        if type(indicator) is not Indicator:
            logger.warning(
                f"Ignoring unknown message type, expected STIX-2 Indicator: {type(indicator)}"
            )
            continue
        if (
            ThreatBusSTIX2Constants.X_THREATBUS_UPDATE.value
            in indicator.object_properties()
            and indicator.x_threatbus_update == Operation.REMOVE.value
        ):
            g_iocs_removed.inc()
            if live_match:
                asyncio.create_task(
                    remove_vast_ioc(vast_binary, vast_endpoint, indicator)
                )
        else:
            # add new Indicator to matcher / query Indicator retrospectively
            g_iocs_added.inc()
            if retro_match:
                asyncio.create_task(
                    retro_match_vast(
                        vast_binary,
                        vast_endpoint,
                        retro_match_max_events,
                        indicator,
                        sightings_queue,
                    )
                )
            if live_match:
                asyncio.create_task(
                    ingest_vast_ioc(vast_binary, vast_endpoint, indicator)
                )
        indicator_queue.task_done()


async def live_match_vast(
    vast_binary: str, vast_endpoint: str, sightings_queue: asyncio.Queue
):
    """
    Starts a VAST matcher. Enqueues all matches from VAST to the
    sightings_queue.
    @param vast_binary The VAST binary command to use with PyVAST
    @param vast_endpoint The endpoint of a running VAST node
    @param sightings_queue The queue to put new sightings into
    @param retro_match Boolean flag to use retro-matching over live-matching
    """
    global logger, matcher_name
    vast = VAST(binary=vast_binary, endpoint=vast_endpoint, logger=logger)
    matcher_name = "threatbus-" + "".join(random.choice(letters) for i in range(10))
    proc = await vast.matcher().start(name=matcher_name).exec()
    # returncode is None as long as the process did not terminate yet
    while proc.returncode is None:
        data = await proc.stdout.readline()
        if not data:
            if not await vast.test_connection():
                logger.error("Lost connection to VAST, cannot live-match")
                # TODO reconnect
            continue
        vast_sighting = data.decode("utf-8").rstrip()
        sighting = matcher_result_to_threatbus_sighting(vast_sighting)
        if not sighting:
            logger.error(f"Cannot parse sighting-output from VAST: {vast_sighting}")
            continue
        g_live_matcher_sightings.inc()
        await sightings_queue.put(sighting)
    stderr = await proc.stderr.read()
    if stderr:
        logger.error(
            "VAST matcher process exited with message: {}".format(stderr.decode())
        )
    logger.critical("Unexpected exit of VAST matcher process.")


async def invoke_cmd_for_context(cmd: str, context: dict, ioc: str = "%ioc"):
    """
    Invoke a command as subprocess for the given context. The command string is
    treated as template string and occurences of "%ioc" are replaced with the
    actually matched IoC.
    Returns stdout from the invoked command.
    @param cmd The command, including flags, to invoke as subprocess. cmd is
        treated as template string and occurrences of '%ioc' are replaced with
        the actually matched IoC.
    @param context The context to forward as JSON
    @param ioc The value to replace '%ioc' with in the `cmd` string
    """
    if not ioc:
        ioc = "%ioc"
    cmd = cmd.replace("%ioc", ioc)
    proc = await asyncio.create_subprocess_exec(
        *lexical_split(cmd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
    )
    proc.stdin.write(json.dumps(context).encode())
    await proc.stdin.drain()
    proc.stdin.close()
    stdout, stderr = await proc.communicate()
    if stderr:
        logger.error(f"Error while transforming sighting context: {stderr}")
    return stdout


async def report_sightings(
    sub_endpoint: str,
    sightings_queue: asyncio.Queue,
    transform_cmd: str = None,
    sink: str = None,
):
    """
    Starts a ZeroMQ publisher on the given endpoint and publishes sightings from
    the sightings_queue.
    @param sub_endpoint A host:port string to connect to via ZeroMQ
    @param sightings_queue The queue to receive sightings from
    @param transform_cmd The command to use to pipe sightings to. Treated
        as template string: occurrences of '%ioc' in the cmd string get replaced
        with the matched IoC.
    @param report_data If True, only report sighting.context.data instead of the
        whole sighting.
    """
    global logger
    if transform_cmd:
        logger.info(
            f"Using '{transform_cmd}' to transform every sighting's context before sending"
        )
    if sink:
        logger.info(f"Forwarding sightings to sink '{sink}'")
    else:
        socket = zmq.Context().socket(zmq.PUB)
        socket.connect(f"tcp://{sub_endpoint}")
        topic = "stix2/sighting"
        logger.info(f"Forwarding sightings to Threat Bus at {sub_endpoint}/{topic}")
    while True:
        sighting = await sightings_queue.get()
        if type(sighting) is not Sighting:
            logger.warning(
                f"Ignoring unknown message type, expected Sighting: {type(sighting)}"
            )
            continue
        if transform_cmd and sighting.context:
            ioc = sighting.ioc
            if sighting.ioc and type(sighting.ioc) is tuple:
                ioc = sighting.ioc[0]  # use first value of tuple
            context_str = await invoke_cmd_for_context(
                transform_cmd, sighting.context, ioc
            )
            try:
                context = json.loads(context_str)
                sighting.context = context
            except Exception as e:
                logger.error(
                    f"Cannot parse transformed sighting context (expecting JSON): {context_str}",
                    e,
                )
                continue
        if sink:
            if sink.lower() == "stdout":
                print(json.dumps(sighting.context))
            else:
                await invoke_cmd_for_context(sink, sighting.context)
        else:
            socket.send_string(f"{topic} {sighting.serialize()}")
        sightings_queue.task_done()
        logger.debug(f"Reported sighting: {sighting}")


def send_manage_message(endpoint: str, action: dict, timeout: int = 5):
    """
    Sends a 'management' message, following the threatbus-zmq-app protocol to
    either subscribe or unsubscribe this application to/from Threat Bus.
    @param endpoint A host:port string to connect to via ZeroMQ
    @param action The message to send as JSON
    @param timeout The period after which the connection attempt is aborted
    """
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect(f"tcp://{endpoint}")
    socket.send_json(action)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    reply = None
    if poller.poll(timeout * 1000):
        reply = socket.recv_json()
    socket.close()
    context.term()
    return reply


def reply_is_success(reply: dict):
    """
    Predicate to check if `reply` is a dict and contains the key-value pair
    "status" = "success"
    @param reply A python dict
    @return True if the dict contains "status" = "success"
    """
    return (
        reply
        and type(reply) is dict
        and reply.get("status", None)
        and reply["status"] == "success"
    )


def subscribe(endpoint: str, topic: str, snapshot: int, timeout: int = 5):
    """
    Subscribes this app to Threat Bus for the given topic. Requests an optional
    snapshot of historical indicators.
    @param endpoint The ZMQ management endpoint of Threat Bus ('host:port')
    @param topic The topic to subscribe to
    @param snapshot An integer value to request n days of historical IoC items
    @param timeout The period after which the connection attempt is aborted
    """
    global logger
    logger.info(f"Subscribing to topic '{topic}'...")
    action = {"action": "subscribe", "topic": topic, "snapshot": snapshot}
    return send_manage_message(endpoint, action, timeout)


def unsubscribe(endpoint: str, topic: str, timeout: int = 5):
    """
    Unsubscribes this app from Threat Bus for the given topic.
    @param endpoint The ZMQ management endpoint of Threat Bus
    @param topic The topic to unsubscribe from
    @param timeout The period after which the connection attempt is aborted
    """
    global logger
    logger.info(f"Unsubscribing from topic '{topic}' ...")
    action = {"action": "unsubscribe", "topic": topic}
    reply = send_manage_message(endpoint, action, timeout)
    if not reply_is_success(reply):
        logger.warning("Unsubscription failed")
        return
    logger.info("Unsubscription successful")


async def heartbeat(endpoint: str, p2p_topic: str, interval: int = 5):
    """
    Sends heartbeats to Threat Bus periodically to check if the given p2p_topic
    is still valid at the Threat Bus host. Cancels all async tasks of this app
    when the heartbeat fails and stops the heartbeat.
    @param endpoint The ZMQ management endpoint of Threat Bus
    @param p2p_topic The topic string to include in the heartbeat
    @param timeout The period after which the connection attempt is aborted
    """
    global logger, async_tasks
    action = {"action": "heartbeat", "topic": p2p_topic}
    while True:
        reply = send_manage_message(endpoint, action, interval)
        if not reply_is_success(reply):
            logger.error("Subscription with Threat Bus host became invalid")
            cancel_async_tasks()
            return
        await asyncio.sleep(interval)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help="Path to a configuration file")
    args = parser.parse_args()

    # we need to use an underscore in the configuration name "pyvast_threatbus"
    # confuse uses the configuration name to lookup environment variables, but
    # it simply upper-cases that name. Dashes are not replaced properly. Using a
    # dash in the configuration name makes it impossible to configure the
    # APPNAMEDIR env variable to overwrite search paths, i.e., in systemd
    # https://confit.readthedocs.io/en/latest/#search-paths
    # https://github.com/beetbox/confuse/blob/v1.4.0/confuse/core.py#L555
    config = confuse.Configuration("pyvast_threatbus")
    config.set_args(args)
    if args.config:
        config.set_file(args.config)

    try:
        validate_config(config)
    except Exception as e:
        sys.exit(ValueError(f"Invalid config: {e}"))

    if config["logging"].get(dict):
        setup_logging_with_config(config["logging"])
    else:
        setup_logging_with_level(config["loglevel"].get(str))

    while True:
        try:
            asyncio.run(
                start(
                    config["vast_binary"].get(),
                    config["vast"].get(),
                    config["threatbus"].get(),
                    config["snapshot"].get(),
                    config["live_match"].get(),
                    config["retro_match"].get(),
                    config["retro_match_max_events"].get(),
                    config["max_background_tasks"].get(),
                    config["metrics"]["interval"].get(),
                    config["metrics"]["filename"].get(),
                    config["transform_context"].get(),
                    config["sink"].get(),
                )
            )
        except asyncio.CancelledError:
            logger.info("Restarting pyvast-threatbus ...")


if __name__ == "__main__":
    main()
