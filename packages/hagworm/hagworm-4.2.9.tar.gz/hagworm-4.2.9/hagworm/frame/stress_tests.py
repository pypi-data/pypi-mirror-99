# -*- coding: utf-8 -*-

from terminal_table import Table

from hagworm.extend.logging import DEFAULT_LOG_FILE_ROTATOR
from hagworm.extend.interface import FunctorInterface, RunnableInterface
from hagworm.extend.asyncio import command
from hagworm.extend.asyncio.base import Utils, MultiTasks, AsyncCirculator
from hagworm.extend.asyncio.zmq import Subscribe, PublishWithBuffer


SIGNAL_PROTOCOL = r'tcp'
SIGNAL_PORT = 0x601
HIGH_WATER_MARK = 0xffffff


class Daemon(command.Daemon):

    async def _run(self):

        with Reporter() as reporter:

            async for _ in AsyncCirculator():

                stopped = self._check_pids()

                await reporter.handle_message()

                if stopped:
                    break

            Utils.log.info(f'\n{reporter.get_report_table()}')


_DEFAULT_DAEMON = Daemon()


class Launcher(command.Launcher):

    def __init__(self,
                 log_file_path=None, log_level=r'INFO',
                 log_file_rotation=DEFAULT_LOG_FILE_ROTATOR, log_file_retention=0xff,
                 subprocess=1, daemon=_DEFAULT_DAEMON, debug=False
                 ):

        super().__init__(
            log_file_path, log_level, log_file_rotation, log_file_retention,
            subprocess, daemon, debug
        )


class Reporter(Subscribe):

    class _Report:

        def __init__(self):
            self.success = []
            self.failure = []

    def __init__(self):

        global SIGNAL_PROTOCOL, SIGNAL_PORT

        super().__init__(f'{SIGNAL_PROTOCOL}://*:{SIGNAL_PORT}', True)

        self._reports = {}

    async def handle_message(self):

        while True:

            message = await self.recv(True)

            if message is None:
                break

            for name, result, resp_time in message:
                if name and result in (r'success', r'failure'):
                    getattr(self._get_report(name), result).append(resp_time)

    def _get_report(self, name: str) -> _Report:

        if name not in self._reports:
            self._reports[name] = self._Report()

        return self._reports[name]

    def open(self):

        global HIGH_WATER_MARK

        super().open(HIGH_WATER_MARK)

    def get_report_table(self) -> str:

        reports = []

        for key, val in self._reports.items():
            reports.append(
                (
                    key,
                    len(val.success),
                    len(val.failure),
                    r'{:.2%}'.format(len(val.success) / (len(val.success) + len(val.failure))),
                    r'{:.3f}s'.format(sum(val.success) / len(val.success) if len(val.success) > 0 else 0),
                    r'{:.3f}s'.format(min(val.success) if len(val.success) > 0 else 0),
                    r'{:.3f}s'.format(max(val.success) if len(val.success) > 0 else 0),
                )
            )

        return Table.create(
            reports,
            (
                r'EventName',
                r'SuccessTotal',
                r'FailureTotal',
                r'SuccessRatio',
                r'SuccessAveTime',
                r'SuccessMinTime',
                r'SuccessMaxTime',
            ),
            use_ansi=False
        )


class TaskInterface(Utils, RunnableInterface):

    def __init__(self, publisher: PublishWithBuffer):

        self._publisher = publisher

    def success(self, name: str, resp_time: int):

        self._publisher.append(
            (name, r'success', resp_time,)
        )

    def failure(self, name: str, resp_time: int):

        self._publisher.append(
            (name, r'failure', resp_time,)
        )

    async def run(self):
        raise NotImplementedError()


class Runner(Utils, FunctorInterface):

    def __init__(self, task_cls: TaskInterface):

        global SIGNAL_PROTOCOL, SIGNAL_PORT

        self._task_cls = task_cls
        self._publisher = PublishWithBuffer(f'{SIGNAL_PROTOCOL}://localhost:{SIGNAL_PORT}', False)

    async def __call__(self, process_id, times, task_num):

        self._publisher.open()

        for _ in range(times):

            tasks = MultiTasks()

            for _ in range(task_num):
                tasks.append(self._task_cls(self._publisher).run())

            await tasks

        await self._publisher.safe_close()
