from timed_task import TimedTask

import time
import threading

tasks = dict()


class TaskExistError(Exception):
    pass


class TaskNotExistError(Exception):
    pass


def add_task(task_obj):
    if not isinstance(task_obj, TimedTask):
        raise TypeError("Make sure task inherit from TimedTask.")
    if task_obj.name in tasks:
        raise TaskExistError("Task: %s already scheduled." % task_obj.name)
    tasks[task_obj.name] = task_obj
    t = threading.Thread(target=task_obj.run)
    t.start()


def remove_task(task_name):
    if task_name not in tasks:
        raise TaskNotExistError("Task: %s not exist." % task_name)
    task_obj = tasks[task_name]
    task_obj.stop()
    del tasks[task_obj.name]


if __name__ == "__main__":
    from task import ShellTask
    task = ShellTask("echo task1")
    start = time.strptime("2019-04-21 16:00:00", "%Y-%m-%d %H:%M:%S")
    end = time.strptime("2019-04-21 16:05:00", "%Y-%m-%d %H:%M:%S")
    timed_task = TimedTask(task, time.mktime(start), time.mktime(end), period=10, name="task1")

    task2 = ShellTask("echo task2")
    timed_task2 = TimedTask(task2, period=5, name="task2")
    print("当前线程数: %s" % threading.active_count())
    add_task(timed_task)
    time.sleep(2)
    print("添加task1后, 当前运行线程数: %s" % threading.active_count())
    add_task(timed_task2)
    time.sleep(2)
    print("添加task2后, 当前运行线程数: %s" % threading.active_count())
    time.sleep(20)
    remove_task("task1")
    time.sleep(2)
    print("删除task1后, 当前运行线程数: %s" % threading.active_count())
    time.sleep(20)
    remove_task("task2")
    time.sleep(2)
    print("删除task2后, 当前运行线程数: %s" % threading.active_count())
