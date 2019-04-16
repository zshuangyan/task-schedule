import time
from util import generate_name
from threading import Event

class TimedTask:
    def __init__(self, task, start=None, end=None, period=60, condition=None, name=None):
        if not name:
            self.name = generate_name()
        else:
            self.name = name
        self.task = task
        self.start = start
        self.end = end
        self.period = period
        self.condition = condition
        self.event = Event()

    def run(self):
        while not self.event.is_set():
            now = time.time()
            if self.start and now < self.start:
                time.sleep(self.start - now)
            elif self.end and now > self.end:
                return
            else:
                if self.task.meet_condition(self.condition):
                    self.task.run()
                time.sleep(self.period)

    def stop(self):
        self.event.set()
