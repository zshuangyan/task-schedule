import time
from threading import Event
from datetime import datetime, timedelta

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class TimeFormatError(Exception):
    pass


class TaskOptionError(Exception):
    pass


class TaskOption:
    def __init__(self, period, start=None, end=None, retry=1):
        self.period = TaskOption.parse_period(period)

        if start:
            try:
                self.start = TaskOption.parse_time(start)
            except Exception:
                raise
        else:
            self.start = start

        if end:
            try:
                self.end = TaskOption.parse_time(end)
            except Exception:
                raise
        else:
            self.end = end

        if not isinstance(retry, int) or retry < 0:
            raise TaskOptionError("retry should equal or larger than 0")
        self.retry = retry

    @staticmethod
    def parse_period(period):
        if isinstance(period, int):
            if period <= 0:
                raise TimeFormatError("period should be positive integer or instance of timedelta")
            return period

        if isinstance(period, timedelta):
            return period.total_seconds()

    @staticmethod
    def parse_time(input_time):
        error_msg = "start or end time should in format: %s or instance of datetime" % TIME_FORMAT

        if isinstance(input_time, str):
            try:
                return time.mktime(time.strptime(input_time, TIME_FORMAT))
            except Exception:
                raise TimeFormatError(error_msg)

        elif isinstance(input_time, datetime):
            return time.mktime(input_time.timetuple())

        else:
            raise TimeFormatError(error_msg)


class TimedTask:
    def __init__(self, name, task, opts):
        self.name = name
        self.task = task
        self.start = opts.start
        self.end = opts.end
        self.period = opts.period
        self.retry = opts.retry
        self.event = Event()

    def run(self):
        while not self.event.is_set():
            now = time.time()
            if self.start and now < self.start:
                time.sleep(self.start - now)
            elif self.end and now > self.end:
                return
            else:
                # 重试直到执行成功为止
                for i in range(self.retry):
                    try:
                        self.task.run()
                    except Exception:
                        pass
                    else:
                        break

                # 执行任务过程中消耗的时间也要算在周期内
                time_elasped = time.time() - now
                time_left = self.period - time_elasped
                if time_left > 0:
                    time.sleep(time_left)

    def stop(self):
        self.event.set()
