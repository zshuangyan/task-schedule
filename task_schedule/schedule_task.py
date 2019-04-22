from task_schedule.timed_task import TimedTask
from task_schedule.task import Task

import threading


class ThreadSafeTask:
    def __init__(self):
        self.tasks = dict()
        self.lock = threading.Lock()

    def exist(self, name):
        return name in self.tasks

    def add(self, name, task, opts):
        if not isinstance(task, Task):
            raise TypeError("Make sure task inherit from Task and implement run method")

        if self.exist(name):
            raise TaskExistError("Task: %s already scheduled" % name)

        t_task = TimedTask(name, task, opts)
        with self.lock:
            self.tasks[name] = t_task
            t = threading.Thread(target=t_task.run)
            t.start()

    def remove(self, name):
        if not self.exist(name):
            raise TaskNotExistError("Task: %s not exist" % name)

        with self.lock:
            t_task = self.tasks[name]
            t_task.stop()
            del self.tasks[name]

    def clear(self):
        with self.lock:
            while self.tasks:
                name, task = self.tasks.popitem()
                task.stop()


class TaskExistError(Exception):
    pass


class TaskNotExistError(Exception):
    pass


sf_tasks = ThreadSafeTask()


def add_task(*args, **kwargs):
    sf_tasks.add(*args, **kwargs)


def remove_task(*args, **kwargs):
    sf_tasks.remove(*args, **kwargs)


def clear_task():
    sf_tasks.clear()
