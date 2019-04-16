from task import Task
from timed_task import TimedTask
import subprocess
import shlex
import time
import threading

class ShellTask(Task):
    def __init__(self, command, timeout=60, *args, **kwargs):
        self.command = command
        self.timeout = timeout

    def run(self, *args, **kwargs):
        if type(self.command) == str:
            self.command = shlex.split(self.command)

        try:
            result = subprocess.run(self.command, 
                                    timeout=self.timeout,
                                    universal_newlines=True)
        except subprocess.CalledProcessError as e:
            return str(e)
        
        else:
            return "stderr: %s\nstdout: %s" % (result.stderr, result.stdout)

    def meet_condition(self, *args, **kwargs):
        return True

tasks = dict()

def add_task(task_obj):
    if not isinstance(task_obj, TimedTask):
        raise TypeError("Make sure task inherit from TimedTask")
    tasks[task_obj.name] = task_obj
    t = threading.Thread(target=task_obj.run)
    t.start()
    

def remove_task(task_obj):
    if not isinstance(task_obj, TimedTask):
        raise TypeError("Make sure task inherit from TimedTask")
    task_obj.stop()
    del tasks[task_obj.name]

if __name__ == "__main__":
    task = ShellTask("date")
    start = time.strptime("2019-04-16 21:52:00", "%Y-%m-%d %H:%M:%S")
    end = time.strptime("2019-04-16 21:55:00", "%Y-%m-%d %H:%M:%S")
    timed_task = TimedTask(task, time.mktime(start), time.mktime(end), 10, name="task1")
    
    task2 = ShellTask("date -R")
    timed_task2 = TimedTask(task2, period=5, name="task2")
    add_task(timed_task)
    time.sleep(10)
    add_task(timed_task2)
    time.sleep(30)
    remove_task(timed_task2)
    time.sleep(20)
    remove_task(timed_task)
