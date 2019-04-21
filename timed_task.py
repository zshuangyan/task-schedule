import time
from util import generate_name
from threading import Event


class TimedTask:
    def __init__(self, task, start=None, end=None, period=60, name=None):
        if not name:
            self.name = generate_name()
        else:
            self.name = name
        self.task = task
        self.start = start
        self.end = end
        self.period = period
        self.event = Event()

    def run(self):
        while not self.event.is_set():
            now = time.time()
            if self.start and now < self.start:
                time.sleep(self.start - now)
            elif self.end and now > self.end:
                return
            else:
                self.task.run()
                # 执行任务过程中消耗的时间也要算在周期内
                time_elasped = time.time() - now
                time_left = self.period - time_elasped
                if time_left > 0:
                    time.sleep(time_left)

    def stop(self):
        self.event.set()
