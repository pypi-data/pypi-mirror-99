# -*- coding: utf-8 -*-
import json
import logging
import socket
import sys
import time
import traceback
from collections import defaultdict
from collections.abc import MutableMapping
from typing import (
    Dict,
    Iterator,
    List,
    ValuesView,
)
from uuid import uuid4

import gevent
import greenlet
import psutil
from gevent.pool import Group

from . import User
from .dispatch import dispatch_users
from .distribution import weight_users
from .exception import RPCError
from .log import greenlet_exception_logger
from .rpc import (
    Message,
    rpc,
)
from .stats import (
    RequestStats,
    setup_distributed_stats_event_listeners,
)

logger = logging.getLogger(__name__)


STATE_INIT, STATE_SPAWNING, STATE_RUNNING, STATE_CLEANUP, STATE_STOPPING, STATE_STOPPED, STATE_MISSING = [
    "ready",
    "spawning",
    "running",
    "cleanup",
    "stopping",
    "stopped",
    "missing",
]
WORKER_REPORT_INTERVAL = 3.0
CPU_MONITOR_INTERVAL = 5.0
HEARTBEAT_INTERVAL = 1
HEARTBEAT_LIVENESS = 3
FALLBACK_INTERVAL = 5


greenlet_exception_handler = greenlet_exception_logger(logger)


class Runner:
    """
    Orchestrates the load test by starting and stopping the users.

    Use one of the :meth:`create_local_runner <locust.env.Environment.create_local_runner>`,
    :meth:`create_master_runner <locust.env.Environment.create_master_runner>` or
    :meth:`create_worker_runner <locust.env.Environment.create_worker_runner>` methods on
    the :class:`Environment <locust.env.Environment>` instance to create a runner of the
    desired type.
    """

    def __init__(self, environment):
        self.environment = environment
        self.user_greenlets = Group()
        self.greenlet = Group()
        self.state = STATE_INIT
        self.spawning_greenlet = None
        self.shape_greenlet = None
        self.shape_last_state = None
        self.current_cpu_usage = 0
        self.cpu_warning_emitted = False
        self.worker_cpu_warning_emitted = False
        self.greenlet.spawn(self.monitor_cpu).link_exception(greenlet_exception_handler)
        self.exceptions = {}
        self.target_user_class_occurrences: Dict[str, int] = {}

        # set up event listeners for recording requests
        def on_request_success(request_type, name, response_time, response_length, **kwargs):
            self.stats.log_request(request_type, name, response_time, response_length)

        def on_request_failure(request_type, name, response_time, response_length, exception, **kwargs):
            self.stats.log_request(request_type, name, response_time, response_length)
            self.stats.log_error(request_type, name, exception)

        self.environment.events.request_success.add_listener(on_request_success)
        self.environment.events.request_failure.add_listener(on_request_failure)
        self.connection_broken = False

        # register listener that resets stats when spawning is complete
        def on_spawning_complete(user_count):
            self.update_state(STATE_RUNNING)
            if environment.reset_stats:
                logger.info("Resetting stats\n")
                self.stats.reset_all()

        self.environment.events.spawning_complete.add_listener(on_spawning_complete)

    def __del__(self):
        # don't leave any stray greenlets if runner is removed
        if self.greenlet and len(self.greenlet) > 0:
            self.greenlet.kill(block=False)

    @property
    def user_classes(self):
        return self.environment.user_classes

    @property
    def user_classes_by_name(self):
        return self.environment.user_classes_by_name

    @property
    def stats(self) -> RequestStats:
        return self.environment.stats

    @property
    def errors(self):
        return self.stats.errors

    @property
    def user_count(self):
        """
        :returns: Number of currently running users
        """
        return len(self.user_greenlets)

    @property
    def user_class_occurrences(self) -> Dict[str, int]:
        """
        :returns: Number of currently running users for each user class
        """
        user_class_occurrences = {user_class.__name__: 0 for user_class in self.user_classes}
        for user_greenlet in self.user_greenlets:
            try:
                user = user_greenlet.args[0]
            except IndexError:
                logger.error(
                    "While calculating number of running users, we encountered a user that didnt have proper args %s",
                    user_greenlet,
                )
                continue
            user_class_occurrences[user.__class__.__name__] += 1
        return user_class_occurrences

    def update_state(self, new_state):
        """
        Updates the current state
        """
        # I (cyberwiz) commented out this logging, because it is too noisy even for debug level
        # Uncomment it if you are specifically debugging state transitions
        # logger.debug("Updating state to '%s', old state was '%s'" % (new_state, self.state))
        self.state = new_state

    def cpu_log_warning(self):
        """Called at the end of the test to repeat the warning & return the status"""
        if self.cpu_warning_emitted:
            logger.warning(
                "CPU usage was too high at some point during the test! See https://docs.locust.io/en/stable/running-locust-distributed.html for how to distribute the load over multiple CPU cores or machines"
            )
            return True
        return False

    def spawn_users(self, user_classes_spawn_count: Dict[str, int], wait: bool = False):
        if self.state == STATE_INIT or self.state == STATE_STOPPED:
            self.update_state(STATE_SPAWNING)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                "Spawning additional %s (%s already running)..."
                % (json.dumps(user_classes_spawn_count), json.dumps(self.user_class_occurrences))
            )
        elif sum(user_classes_spawn_count.values()) > 0:
            logger.info(
                "Spawning additional %s (%s already running)..."
                % (sum(user_classes_spawn_count.values()), sum(self.user_class_occurrences.values()))
            )

        def spawn(user_class: str, spawn_count: int):
            n = 0
            while n < spawn_count:
                new_user = self.user_classes_by_name[user_class](self.environment)
                new_user.start(self.user_greenlets)
                n += 1
                if n % 10 == 0 or n == spawn_count:
                    logger.debug("%i users spawned" % self.user_count)
            logger.debug("All users of class %s spawned" % user_class)

        for user_class, spawn_count in user_classes_spawn_count.items():
            spawn(user_class, spawn_count)

        if wait:
            self.user_greenlets.join()
            logger.info("All users stopped\n")

    def stop_users(self, user_classes_stop_count: Dict[str, int]):
        async_calls_to_stop = Group()
        stop_group = Group()

        for user_class, stop_count in user_classes_stop_count.items():
            if self.user_class_occurrences[user_class] == 0:
                continue

            to_stop = []
            for user_greenlet in self.user_greenlets:
                if len(to_stop) == stop_count:
                    break
                try:
                    user = user_greenlet.args[0]
                except IndexError:
                    logger.error(
                        "While stopping users, we encountered a user that didnt have proper args %s", user_greenlet
                    )
                    continue
                if isinstance(user, self.user_classes_by_name[user_class]):
                    to_stop.append(user)

            if not to_stop:
                continue

            while True:
                user_to_stop: User = to_stop.pop()
                logger.debug("Stopping %s" % user_to_stop.greenlet.name)
                if user_to_stop.greenlet is greenlet.getcurrent():
                    # User called runner.quit(), so don't block waiting for killing to finish
                    user_to_stop.group.killone(user_to_stop.greenlet, block=False)
                elif self.environment.stop_timeout:
                    async_calls_to_stop.add(gevent.spawn_later(0, User.stop, user_to_stop, force=False))
                    stop_group.add(user_to_stop.greenlet)
                else:
                    async_calls_to_stop.add(gevent.spawn_later(0, User.stop, user_to_stop, force=True))
                if not to_stop:
                    break

        async_calls_to_stop.join()

        if not stop_group.join(timeout=self.environment.stop_timeout):
            logger.info(
                "Not all users finished their tasks & terminated in %s seconds. Stopping them..."
                % self.environment.stop_timeout
            )
            stop_group.kill(block=True)

        msg = "%i Users have been stopped, %g still running" % (sum(user_classes_stop_count.values()), self.user_count)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(msg)
        elif sum(user_classes_stop_count.values()) > 0:
            logger.info(msg)

    def monitor_cpu(self):
        process = psutil.Process()
        while True:
            self.current_cpu_usage = process.cpu_percent()
            if self.current_cpu_usage > 90 and not self.cpu_warning_emitted:
                logging.warning(
                    "CPU usage above 90%! This may constrain your throughput and may even give inconsistent response time measurements! See https://docs.locust.io/en/stable/running-locust-distributed.html for how to distribute the load over multiple CPU cores or machines"
                )
                self.cpu_warning_emitted = True
            gevent.sleep(CPU_MONITOR_INTERVAL)

    def start(self, user_count: int, spawn_rate: float, wait: bool = False):
        """
        Start running a load test

        :param user_count: Total number of users to start
        :param spawn_rate: Number of users to spawn per second
        :param wait: If True calls to this method will block until all users are spawned.
                     If False (the default), a greenlet that spawns the users will be
                     started and the call to this method will return immediately.
        """
        if self.state != STATE_RUNNING and self.state != STATE_SPAWNING:
            self.stats.clear_all()
            self.exceptions = {}
            self.cpu_warning_emitted = False
            self.worker_cpu_warning_emitted = False

        if wait and user_count - self.user_count > spawn_rate:
            raise ValueError("wait is True but the amount of users to add is greater than the spawn rate")

        for user_class in self.user_classes:
            if self.environment.host is not None:
                user_class.host = self.environment.host

        self.target_user_class_occurrences = weight_users(self.user_classes, user_count)

        # Dummy worker node since dispatch_users needs it
        dummy_worker_node = WorkerNode(id="dummy")
        dummy_worker_node.user_class_occurrences = self.user_class_occurrences

        users_dispatcher = dispatch_users(
            worker_nodes=[dummy_worker_node],
            user_class_occurrences=self.target_user_class_occurrences,
            spawn_rate=spawn_rate,
        )

        if self.state != STATE_INIT and self.state != STATE_STOPPED:
            logger.debug(
                "Updating running test with %d users, %.2f spawn rate and wait=%r" % (user_count, spawn_rate, wait)
            )
            self.update_state(STATE_SPAWNING)

        try:
            for dispatched_users in users_dispatcher:
                user_classes_spawn_count = {}
                user_classes_stop_count = {}
                user_class_occurrences = dispatched_users[dummy_worker_node.id]
                logger.info("Updating running test with %d users" % (sum(user_class_occurrences.values()),))
                for user_class, occurrences in user_class_occurrences.items():
                    logger.debug(
                        "Updating running test with %d users of class %s and wait=%r" % (occurrences, user_class, wait)
                    )
                    if self.user_class_occurrences[user_class] > occurrences:
                        user_classes_stop_count[user_class] = self.user_class_occurrences[user_class] - occurrences
                    elif self.user_class_occurrences[user_class] < occurrences:
                        user_classes_spawn_count[user_class] = occurrences - self.user_class_occurrences[user_class]

                if wait:
                    # spawn_users will block, so we need to call stop_users first
                    self.stop_users(user_classes_stop_count)
                    self.spawn_users(user_classes_spawn_count, wait)
                else:
                    # call spawn_users before stopping the users since stop_users
                    # can be blocking because of the stop_timeout
                    self.spawn_users(user_classes_spawn_count, wait)
                    self.stop_users(user_classes_stop_count)

        except KeyboardInterrupt:
            # We need to catch keyboard interrupt. Otherwise, if KeyboardInterrupt is received while in
            # a gevent.sleep inside the dispatch_users function, locust won't gracefully shutdown.
            self.quit()

        logger.info(
            "All users spawned: %s (%i total running)"
            % (
                ", ".join("%s: %d" % (name, count) for name, count in self.user_class_occurrences.items()),
                sum(self.user_class_occurrences.values()),
            )
        )

        self.environment.events.spawning_complete.fire(user_count=sum(self.target_user_class_occurrences.values()))

    def start_shape(self):
        if self.shape_greenlet:
            logger.info("There is an ongoing shape test running. Editing is disabled")
            return

        logger.info("Shape test starting. User count and spawn rate are ignored for this type of load test")
        self.update_state(STATE_INIT)
        self.shape_greenlet = self.greenlet.spawn(self.shape_worker)
        self.shape_greenlet.link_exception(greenlet_exception_handler)
        self.environment.shape_class.reset_time()

    def shape_worker(self):
        logger.info("Shape worker starting")
        while self.state == STATE_INIT or self.state == STATE_SPAWNING or self.state == STATE_RUNNING:
            new_state = self.environment.shape_class.tick()
            if new_state is None:
                logger.info("Shape test stopping")
                if self.environment.parsed_options and self.environment.parsed_options.headless:
                    self.quit()
                else:
                    self.stop()
                self.shape_greenlet = None
                self.shape_last_state = None
                return
            elif self.shape_last_state == new_state:
                gevent.sleep(1)
            else:
                user_count, spawn_rate = new_state
                logger.info("Shape test updating to %d users at %.2f spawn rate" % (user_count, spawn_rate))
                self.start(user_count=user_count, spawn_rate=spawn_rate)
                self.shape_last_state = new_state

    def stop(self):
        """
        Stop a running load test by stopping all running users
        """
        logger.debug("Stopping all users")
        self.update_state(STATE_CLEANUP)

        # if we are currently spawning users we need to kill the spawning greenlet first
        if self.spawning_greenlet and not self.spawning_greenlet.ready():
            self.spawning_greenlet.kill(block=True)

        if self.environment.shape_class is not None and self.shape_greenlet is not greenlet.getcurrent():
            # If the test was not started yet and that locust is
            # stopped/quit, shape_greenlet will be None.
            if self.shape_greenlet is not None:
                self.shape_greenlet.kill(block=True)
                self.shape_greenlet = None
            self.shape_last_state = None

        self.stop_users(self.user_class_occurrences)

        self.update_state(STATE_STOPPED)

        self.cpu_log_warning()

    def quit(self):
        """
        Stop any running load test and kill all greenlets for the runner
        """
        self.stop()
        self.greenlet.kill(block=True)

    def log_exception(self, node_id, msg, formatted_tb):
        key = hash(formatted_tb)
        row = self.exceptions.setdefault(key, {"count": 0, "msg": msg, "traceback": formatted_tb, "nodes": set()})
        row["count"] += 1
        row["nodes"].add(node_id)
        self.exceptions[key] = row

    @property
    def target_user_count(self) -> int:
        return sum(self.target_user_class_occurrences.values())


class LocalRunner(Runner):
    """
    Runner for running single process load test
    """

    def __init__(self, environment):
        """
        :param environment: Environment instance
        """
        super().__init__(environment)

        # register listener thats logs the exception for the local runner
        def on_user_error(user_instance, exception, tb):
            formatted_tb = "".join(traceback.format_tb(tb))
            self.log_exception("local", str(exception), formatted_tb)

        self.environment.events.user_error.add_listener(on_user_error)

    def start(self, user_count: int, spawn_rate: float, wait: bool = False):
        if spawn_rate > 100:
            logger.warning(
                "Your selected spawn rate is very high (>100), and this is known to sometimes cause issues. Do you really need to ramp up that fast?"
            )

        if self.state != STATE_RUNNING and self.state != STATE_SPAWNING:
            # if we're not already running we'll fire the test_start event
            self.environment.events.test_start.fire(environment=self.environment)

        if self.spawning_greenlet:
            # kill existing spawning_greenlet before we start a new one
            self.spawning_greenlet.kill(block=True)
        self.spawning_greenlet = self.greenlet.spawn(
            lambda: super(LocalRunner, self).start(user_count, spawn_rate, wait=wait)
        )
        self.spawning_greenlet.link_exception(greenlet_exception_handler)

    def stop(self):
        if self.state == STATE_STOPPED:
            return
        super().stop()
        self.environment.events.test_stop.fire(environment=self.environment)


class DistributedRunner(Runner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setup_distributed_stats_event_listeners(self.environment.events, self.stats)


class WorkerNode:
    def __init__(self, id: str, state=STATE_INIT, heartbeat_liveness=HEARTBEAT_LIVENESS):
        self.id: str = id
        self.state = state
        self.heartbeat = heartbeat_liveness
        self.cpu_usage = 0
        self.cpu_warning_emitted = False
        self.user_class_occurrences: Dict[str, int] = {}

    @property
    def user_count(self) -> int:
        return sum(self.user_class_occurrences.values())


class WorkerNodes(MutableMapping):
    def __init__(self):
        self._worker_nodes = {}

    def get_by_state(self, state) -> List[WorkerNode]:
        return [c for c in self.values() if c.state == state]

    @property
    def all(self) -> ValuesView[WorkerNode]:
        return self.values()

    @property
    def ready(self) -> List[WorkerNode]:
        return self.get_by_state(STATE_INIT)

    @property
    def spawning(self) -> List[WorkerNode]:
        return self.get_by_state(STATE_SPAWNING)

    @property
    def running(self) -> List[WorkerNode]:
        return self.get_by_state(STATE_RUNNING)

    @property
    def missing(self) -> List[WorkerNode]:
        return self.get_by_state(STATE_MISSING)

    def __setitem__(self, k: str, v: WorkerNode) -> None:
        self._worker_nodes[k] = v

    def __delitem__(self, k: str) -> None:
        del self._worker_nodes[k]

    def __getitem__(self, k: str) -> WorkerNode:
        return self._worker_nodes[k]

    def __len__(self) -> int:
        return len(self._worker_nodes)

    def __iter__(self) -> Iterator[WorkerNode]:
        return iter(self._worker_nodes)


class MasterRunner(DistributedRunner):
    """
    Runner used to run distributed load tests across multiple processes and/or machines.

    MasterRunner doesn't spawn any user greenlets itself. Instead it expects
    :class:`WorkerRunners <WorkerRunner>` to connect to it, which it will then direct
    to start and stop user greenlets. Stats sent back from the
    :class:`WorkerRunners <WorkerRunner>` will aggregated.
    """

    def __init__(self, environment, master_bind_host, master_bind_port):
        """
        :param environment: Environment instance
        :param master_bind_host: Host/interface to use for incoming worker connections
        :param master_bind_port: Port to use for incoming worker connections
        """
        super().__init__(environment)
        self.worker_cpu_warning_emitted = False
        self.master_bind_host = master_bind_host
        self.master_bind_port = master_bind_port
        self.spawn_rate: float = 0

        self.clients = WorkerNodes()
        try:
            self.server = rpc.Server(master_bind_host, master_bind_port)
        except RPCError as e:
            if e.args[0] == "Socket bind failure: Address already in use":
                port_string = master_bind_host + ":" + master_bind_port if master_bind_host != "*" else master_bind_port
                logger.error(
                    f"The Locust master port ({port_string}) was busy. Close any applications using that port - perhaps an old instance of Locust master is still running? ({e.args[0]})"
                )
                sys.exit(1)
            else:
                raise

        self.greenlet.spawn(self.heartbeat_worker).link_exception(greenlet_exception_handler)
        self.greenlet.spawn(self.client_listener).link_exception(greenlet_exception_handler)

        # listener that gathers info on how many users the worker has spawned
        def on_worker_report(client_id, data):
            if client_id not in self.clients:
                logger.info("Discarded report from unrecognized worker %s", client_id)
                return
            self.clients[client_id].user_class_occurrences = data["user_class_occurrences"]

        self.environment.events.worker_report.add_listener(on_worker_report)

        # register listener that sends quit message to worker nodes
        def on_quitting(environment, **kw):
            self.quit()

        self.environment.events.quitting.add_listener(on_quitting)

    @property
    def user_count(self) -> int:
        return sum(c.user_count for c in self.clients.values())

    def cpu_log_warning(self):
        warning_emitted = Runner.cpu_log_warning(self)
        if self.worker_cpu_warning_emitted:
            logger.warning("CPU usage threshold was exceeded on workers during the test!")
            warning_emitted = True
        return warning_emitted

    def start(self, user_count: int, spawn_rate: float, **kwargs) -> None:
        num_workers = len(self.clients.ready) + len(self.clients.running) + len(self.clients.spawning)
        if not num_workers:
            logger.warning(
                "You are running in distributed mode but have no worker servers connected. "
                "Please connect workers prior to swarming."
            )
            return

        for user_class in self.user_classes:
            if self.environment.host is not None:
                user_class.host = self.environment.host

        self.target_user_class_occurrences = weight_users(self.user_classes, user_count)

        self.spawn_rate = spawn_rate

        worker_spawn_rate = float(spawn_rate) / (num_workers or 1)
        logger.info(
            "Sending spawn jobs of %d users and %.2f spawn rate to %d ready clients"
            % (user_count, worker_spawn_rate, num_workers)
        )

        if worker_spawn_rate > 100:
            logger.warning(
                "Your selected spawn rate is very high (>100/worker), and this is known to sometimes cause issues. Do you really need to ramp up that fast?"
            )

        if self.state != STATE_RUNNING and self.state != STATE_SPAWNING:
            self.stats.clear_all()
            self.exceptions = {}
            self.environment.events.test_start.fire(environment=self.environment)

        self.update_state(STATE_SPAWNING)

        users_dispatcher = dispatch_users(
            worker_nodes=self.clients.ready + self.clients.running + self.clients.spawning,
            user_class_occurrences=self.target_user_class_occurrences,
            spawn_rate=spawn_rate,
        )

        try:
            for dispatched_users in users_dispatcher:
                dispatch_greenlets = Group()
                for worker_node_id, worker_user_class_occurrences in dispatched_users.items():
                    data = {
                        "timestamp": time.time(),
                        "user_class_occurrences": worker_user_class_occurrences,
                        "host": self.environment.host,
                        "stop_timeout": self.environment.stop_timeout,
                    }
                    dispatch_greenlets.add(
                        gevent.spawn_later(
                            0,
                            self.server.send_to_client,
                            Message("spawn", data, worker_node_id),
                        )
                    )
                logger.debug("Sending spawn message to %i client(s)" % len(dispatch_greenlets))
                dispatch_greenlets.join()

        except KeyboardInterrupt:
            # We need to catch keyboard interrupt. Otherwise, if KeyboardInterrupt is received while in
            # a gevent.sleep inside the dispatch_users function, locust won't gracefully shutdown.
            self.quit()

        # Wait a little for workers to report their users to the master
        # so that we can give an accurate log message below, i.e. "All users spawned [...]".
        # Otherwise, the logged user count might be less than the target user count.
        timeout = gevent.Timeout(0.1)
        timeout.start()
        try:
            while self.user_count != self.target_user_count:
                gevent.sleep()
        except gevent.Timeout:
            pass
        finally:
            timeout.cancel()

        logger.info(
            "All users spawned: %s (%i total running)"
            % (
                ", ".join("%s: %d" % (name, count) for name, count in self.reported_user_class_occurrences.items()),
                sum(self.reported_user_class_occurrences.values()),
            )
        )

    def stop(self):
        if self.state not in [STATE_INIT, STATE_STOPPED, STATE_STOPPING]:
            logger.debug("Stopping...")
            self.update_state(STATE_STOPPING)

            if self.environment.shape_class is not None and self.shape_greenlet is not greenlet.getcurrent():
                self.shape_greenlet.kill(block=True)
                self.shape_greenlet = None
                self.shape_last_state = None

            for client in self.clients.all:
                logger.debug("Sending stop message to client %s" % client.id)
                self.server.send_to_client(Message("stop", None, client.id))

            # Give an additional 60s for all workers to stop
            timeout = gevent.Timeout(self.environment.stop_timeout or 0 + 60)
            timeout.start()
            try:
                while self.user_count != 0:
                    gevent.sleep(1)
            except gevent.Timeout:
                logger.error("Timeout waiting for all workers to stop")
            finally:
                timeout.cancel()

            self.environment.events.test_stop.fire(environment=self.environment)

    def quit(self):
        self.stop()
        logger.debug("Quitting...")
        for client in self.clients.all:
            logger.debug("Sending quit message to client %s" % (client.id))
            self.server.send_to_client(Message("quit", None, client.id))
        gevent.sleep(0.5)  # wait for final stats report from all workers
        self.greenlet.kill(block=True)

    def check_stopped(self):
        if (
            not self.state == STATE_INIT
            and not self.state == STATE_STOPPED
            and all(map(lambda x: x.state != STATE_RUNNING and x.state != STATE_SPAWNING, self.clients.all))
        ):
            self.update_state(STATE_STOPPED)

    def heartbeat_worker(self):
        while True:
            gevent.sleep(HEARTBEAT_INTERVAL)
            if self.connection_broken:
                self.reset_connection()
                continue

            for client in self.clients.all:
                if client.heartbeat < 0 and client.state != STATE_MISSING:
                    logger.info("Worker %s failed to send heartbeat, setting state to missing." % str(client.id))
                    client.state = STATE_MISSING
                    client.user_class_occurrences = {}
                    if self.worker_count <= 0:
                        logger.info("The last worker went missing, stopping test.")
                        self.stop()
                        self.check_stopped()
                else:
                    client.heartbeat -= 1

    def reset_connection(self):
        logger.info("Reset connection to worker")
        try:
            self.server.close()
            self.server = rpc.Server(self.master_bind_host, self.master_bind_port)
        except RPCError as e:
            logger.error("Temporary failure when resetting connection: %s, will retry later." % (e))

    def client_listener(self):
        while True:
            try:
                client_id, msg = self.server.recv_from_client()
            except RPCError as e:
                logger.error("RPCError found when receiving from client: %s" % (e))
                self.connection_broken = True
                gevent.sleep(FALLBACK_INTERVAL)
                continue
            self.connection_broken = False
            msg.node_id = client_id
            if msg.type == "client_ready":
                worker_node_id = msg.node_id
                self.clients[worker_node_id] = WorkerNode(worker_node_id, heartbeat_liveness=HEARTBEAT_LIVENESS)
                logger.info(
                    "Client %r reported as ready. Currently %i clients ready to swarm."
                    % (worker_node_id, len(self.clients.ready + self.clients.running + self.clients.spawning))
                )
                if self.state == STATE_RUNNING or self.state == STATE_SPAWNING:
                    # balance the load distribution when new client joins
                    self.start(self.target_user_count, self.spawn_rate)
                # emit a warning if the worker's clock seem to be out of sync with our clock
                # if abs(time() - msg.data["time"]) > 5.0:
                #    warnings.warn("The worker node's clock seem to be out of sync. For the statistics to be correct the different locust servers need to have synchronized clocks.")
            elif msg.type == "client_stopped":
                del self.clients[msg.node_id]
                logger.info("Removing %s client from running clients" % (msg.node_id))
            elif msg.type == "heartbeat":
                if msg.node_id in self.clients:
                    c = self.clients[msg.node_id]
                    c.heartbeat = HEARTBEAT_LIVENESS
                    client_state = msg.data["state"]
                    if c.state == STATE_MISSING:
                        logger.info(
                            "Worker %s self-healed with heartbeat, setting state to %s." % (str(c.id), client_state)
                        )
                        user_class_occurrences = msg.data.get("user_class_occurrences")
                        if user_class_occurrences:
                            c.user_class_occurrences = user_class_occurrences
                    c.state = client_state
                    c.cpu_usage = msg.data["current_cpu_usage"]
                    if not c.cpu_warning_emitted and c.cpu_usage > 90:
                        self.worker_cpu_warning_emitted = True  # used to fail the test in the end
                        c.cpu_warning_emitted = True  # used to suppress logging for this node
                        logger.warning(
                            "Worker %s exceeded cpu threshold (will only log this once per worker)" % (msg.node_id)
                        )
            elif msg.type == "stats":
                self.environment.events.worker_report.fire(client_id=msg.node_id, data=msg.data)
            elif msg.type == "spawning":
                self.clients[msg.node_id].state = STATE_SPAWNING
            elif msg.type == "spawning_complete":
                self.clients[msg.node_id].state = STATE_RUNNING
                self.clients[msg.node_id].user_class_occurrences = msg.data["user_class_occurrences"]
                if len(self.clients.spawning) == 0:
                    self.environment.events.spawning_complete.fire(
                        user_count=sum(self.target_user_class_occurrences.values())
                    )
            elif msg.type == "quit":
                if msg.node_id in self.clients:
                    del self.clients[msg.node_id]
                    logger.info(
                        "Client %r quit. Currently %i clients connected." % (msg.node_id, len(self.clients.ready))
                    )
                    if self.worker_count - len(self.clients.missing) <= 0:
                        logger.info("The last worker quit, stopping test.")
                        self.stop()
                        if self.environment.parsed_options and self.environment.parsed_options.headless:
                            self.quit()
            elif msg.type == "exception":
                self.log_exception(msg.node_id, msg.data["msg"], msg.data["traceback"])

            self.check_stopped()

    @property
    def worker_count(self):
        return len(self.clients.ready) + len(self.clients.spawning) + len(self.clients.running)

    @property
    def reported_user_class_occurrences(self) -> Dict[str, int]:
        reported_user_class_occurrences = defaultdict(lambda: 0)
        for client in self.clients.ready + self.clients.spawning + self.clients.running:
            for name, count in client.user_class_occurrences.items():
                reported_user_class_occurrences[name] += count
        return reported_user_class_occurrences


class WorkerRunner(DistributedRunner):
    """
    Runner used to run distributed load tests across multiple processes and/or machines.

    WorkerRunner connects to a :class:`MasterRunner` from which it'll receive
    instructions to start and stop user greenlets. The WorkerRunner will periodically
    take the stats generated by the running users and send back to the :class:`MasterRunner`.
    """

    def __init__(self, environment, master_host, master_port):
        """
        :param environment: Environment instance
        :param master_host: Host/IP to use for connection to the master
        :param master_port: Port to use for connecting to the master
        """
        super().__init__(environment)
        self.worker_state = STATE_INIT
        self.client_id = socket.gethostname() + "_" + uuid4().hex
        self.master_host = master_host
        self.master_port = master_port
        self.worker_cpu_warning_emitted = False
        self.client = rpc.Client(master_host, master_port, self.client_id)
        self.greenlet.spawn(self.heartbeat).link_exception(greenlet_exception_handler)
        self.greenlet.spawn(self.worker).link_exception(greenlet_exception_handler)
        self.client.send(Message("client_ready", None, self.client_id))
        self.greenlet.spawn(self.stats_reporter).link_exception(greenlet_exception_handler)

        # register listener for when all users have spawned, and report it to the master node
        def on_spawning_complete(user_count):
            assert user_count == sum(self.user_class_occurrences.values())
            self.client.send(
                Message("spawning_complete", {"user_class_occurrences": self.user_class_occurrences}, self.client_id)
            )
            self.worker_state = STATE_RUNNING

        self.environment.events.spawning_complete.add_listener(on_spawning_complete)

        # register listener that adds the current number of spawned users to the report that is sent to the master node
        def on_report_to_master(client_id, data):
            data["user_class_occurrences"] = self.user_class_occurrences

        self.environment.events.report_to_master.add_listener(on_report_to_master)

        # register listener that sends quit message to master
        def on_quitting(environment, **kw):
            self.client.send(Message("quit", None, self.client_id))

        self.environment.events.quitting.add_listener(on_quitting)

        # register listener thats sends user exceptions to master
        def on_user_error(user_instance, exception, tb):
            formatted_tb = "".join(traceback.format_tb(tb))
            self.client.send(Message("exception", {"msg": str(exception), "traceback": formatted_tb}, self.client_id))

        self.environment.events.user_error.add_listener(on_user_error)

    def start(self, user_count, spawn_rate, wait=False):
        raise NotImplementedError("use start_worker")

    def start_worker(self, user_class_occurrences: Dict[str, int], **kwargs):
        """
        Start running a load test as a worker

        :param user_class_occurrences: Users to run
        """
        self.target_user_class_occurrences = user_class_occurrences

        if self.worker_state != STATE_RUNNING and self.worker_state != STATE_SPAWNING:
            self.stats.clear_all()
            self.exceptions = {}
            self.cpu_warning_emitted = False
            self.worker_cpu_warning_emitted = False

        user_classes_spawn_count = {}
        user_classes_stop_count = {}

        for user_class, occurrences in user_class_occurrences.items():
            if self.user_class_occurrences[user_class] > occurrences:
                user_classes_stop_count[user_class] = self.user_class_occurrences[user_class] - occurrences
            elif self.user_class_occurrences[user_class] < occurrences:
                user_classes_spawn_count[user_class] = occurrences - self.user_class_occurrences[user_class]

        # call spawn_users before stopping the users since stop_users
        # can be blocking because of the stop_timeout
        self.spawn_users(user_classes_spawn_count)
        self.stop_users(user_classes_stop_count)

        self.environment.events.spawning_complete.fire(user_count=sum(self.user_class_occurrences.values()))

    def heartbeat(self):
        while True:
            try:
                self.client.send(
                    Message(
                        "heartbeat",
                        {
                            "state": self.worker_state,
                            "current_cpu_usage": self.current_cpu_usage,
                            "user_class_occurrences": self.user_class_occurrences,
                        },
                        self.client_id,
                    )
                )
            except RPCError as e:
                logger.error("RPCError found when sending heartbeat: %s" % (e))
                self.reset_connection()
            gevent.sleep(HEARTBEAT_INTERVAL)

    def reset_connection(self):
        logger.info("Reset connection to master")
        try:
            self.client.close()
            self.client = rpc.Client(self.master_host, self.master_port, self.client_id)
        except RPCError as e:
            logger.error("Temporary failure when resetting connection: %s, will retry later." % (e))

    def worker(self):
        last_received_spawn_timestamp = 0
        while True:
            try:
                msg = self.client.recv()
            except RPCError as e:
                logger.error("RPCError found when receiving from master: %s" % (e))
                continue
            if msg.type == "spawn":
                self.worker_state = STATE_SPAWNING
                self.client.send(Message("spawning", None, self.client_id))
                job = msg.data
                if job["timestamp"] <= last_received_spawn_timestamp:
                    logger.info(
                        "Discard spawn message with older or equal timestamp than timestamp of previous spawn message"
                    )
                    continue
                self.environment.host = job["host"]
                self.environment.stop_timeout = job["stop_timeout"]
                if self.spawning_greenlet:
                    # kill existing spawning greenlet before we launch new one
                    self.spawning_greenlet.kill(block=True)
                self.spawning_greenlet = self.greenlet.spawn(lambda: self.start_worker(job["user_class_occurrences"]))
                self.spawning_greenlet.link_exception(greenlet_exception_handler)
                last_received_spawn_timestamp = job["timestamp"]
            elif msg.type == "stop":
                self.stop()
                self.client.send(Message("client_stopped", None, self.client_id))
                self.client.send(Message("client_ready", None, self.client_id))
                self.worker_state = STATE_INIT
            elif msg.type == "quit":
                logger.info("Got quit message from master, shutting down...")
                self.stop()
                self._send_stats()  # send a final report, in case there were any samples not yet reported
                self.greenlet.kill(block=True)

    def stats_reporter(self):
        while True:
            try:
                self._send_stats()
            except RPCError as e:
                logger.error("Temporary connection lost to master server: %s, will retry later." % (e))
            gevent.sleep(WORKER_REPORT_INTERVAL)

    def _send_stats(self):
        data = {}
        self.environment.events.report_to_master.fire(client_id=self.client_id, data=data)
        self.client.send(Message("stats", data, self.client_id))
