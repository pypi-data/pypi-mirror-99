import asyncio
from concurrent import futures
import errno
import logging
import uuid
import warnings

from ..core import BaseClient, LoopHelper
from .external_task_worker import ExternalTaskWorker

logger = logging.getLogger(__name__)

class ExternalTaskClient(BaseClient):

    def __init__(self, url, session=None, identity=None, loop=None):
        super(ExternalTaskClient, self).__init__(url, session, identity)

        if loop is None:
            loop = asyncio.get_event_loop()

        self.__loop_helper = LoopHelper(loop, on_shutdown=self.__on_shutdown)
        self.__worker_id = str(uuid.uuid4())

        self._topic_for_handler = {}

    def subscribe_to_external_task_for_topic(self, topic, handler, **task_options):
        warnings.warn("Please use 'subscribe_to_external_task_topic' instead of 'subscribe_to_external_task_for_topic'.", DeprecationWarning)
        self.subscribe_to_external_task_topic(topic, handler, **task_options)

    def subscribe_to_external_task_topic(self, topic, handler, **task_options):
        """
        task_options:
            - max_tasks
            - long_polling_timeout
            - lock_duration
            - additional_duration
            - extend_lock_timeout
        """
        if topic in self._topic_for_handler:
            logger.warning(f"The topic '{topic}' skipped, is already registered.'")
        else:
            self.__start_subscription(topic, handler, task_options)

    def __start_subscription(self, topic, handler, task_options):
        async def bg_job_handle_external_tasks():
            try:
                await self.handle_external_tasks(topic, handler, task_options)
            except Exception as e:
                if type(e) is errno.EPIPE:
                    # Raised while long polling finished, that the reason for only log as info.
                    logger.info(f"expected long pollng error: {e}")
                else:
                    import traceback
                    import sys
                    traceback.print_exc(file=sys.stdout)
                    logger.warn(f"exception on handle_external_task: {e}")

        async_bg_task = self.__loop_helper.register_background_task(bg_job_handle_external_tasks)
        self._topic_for_handler[topic] = async_bg_task

    def subscribe_to_external_tasks_for_topics(self, topics_for_handlers):
        for topic in topics_for_handlers.keys():
            handler = topics_for_handlers[topic] # TODO: Options sollten auch hier zu setzen sein

            self.subscribe_to_external_task_for_topic(topic, handler)

    def start(self, run_forever=True):
        logger.info(f"Starting external task for topics '{', '.join(self._topic_for_handler.keys())}'.")
        logger.info(f"Connecting to process engine at url '{self._url}'.")
        self.__loop_helper.start(run_forever=run_forever)

    async def handle_external_tasks(self, topic, handler, task_options):
        external_tasks = await self.__fetch_and_lock(topic, handler, task_options)

        len_external_tasks = len(external_tasks)
        if len_external_tasks >= 1:
            logger.info(f"receive {len_external_tasks} tasks for topic '{topic}'.")

            external_task_tasks = []

            external_task_options = {}

            if task_options.get("additional_lock_duration", None):
                external_task_options["additional_lock_duration"] = task_options["additional_lock_duration"]

            # EXTEND_LOCK_TIMEOUT
            if task_options.get("extend_lock_timeout", None):
                external_task_options["extend_lock_timeout"] = task_options["extend_lock_timeout"]

            for external_task in external_tasks:
                external_task_worker = ExternalTaskWorker(
                    self._url, 
                    self._session, 
                    self._identity, 
                    self.__loop_helper,
                    handler, 
                    external_task,
                    external_task_options)
                task = external_task_worker.start()
                external_task_tasks.append(task)

            try:
                done_tasks, pending = await asyncio.wait(external_task_tasks, return_when=futures.ALL_COMPLETED)
                logger.debug(f"Wait result while handle external task (done: {done_tasks}, pending {pending}).")
            except Exception as e:
                logger.error(f"asyncio.wait({e} - {type(e)})")

    async def __on_shutdown(self):
        await self.close()

    def stop(self):
        logger.info(f"Stopping external task for topics {self._topic_for_handler.keys()}")
        self.__loop_helper.stop()

    async def __fetch_and_lock(self, topic, handler, task_options={}):
        logger.info(f"fetch and lock external task for topic {topic} and options {task_options}")

        max_tasks = task_options.get('max_tasks', 10)
        long_polling_timeout = task_options.get('long_polling_timeout', (10 * 1000))
        lock_duration = task_options.get('lock_duration', (100 * 1000))

        request = {
            "workerId": self.__worker_id,
            "topicName": topic,
            "maxTasks": max_tasks,
            "longPollingTimeout": long_polling_timeout,
            "lockDuration": lock_duration
        }

        external_tasks = await self.do_post('/atlas_engine/api/v1/external_tasks/fetch_and_lock', request)

        logger.debug(f"receive {len(external_tasks)} for topic {topic}.")

        return external_tasks
