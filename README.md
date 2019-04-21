# task-schedule
基于多线程和事件实现的定时任务，系统已实现了Shell命令执行的任务, 使用方法示例：  
```
from task-schedule.schedule_task import ShellTask, TimedTask
task1 = ShellTask("date")
start = time.strptime("2019-04-16 21:52:00", "%Y-%m-%d %H:%M:%S")
end = time.strptime("2019-04-16 21:55:00", "%Y-%m-%d %H:%M:%S")
timed_task1 = TimedTask(task1, time.mktime(start), time.mktime(end), 10, name="task1")

task2 = ShellTask("date -R")
timed_task2 = TimedTask(task2, period=5, name="task2")

add_task(timed_task)
time.sleep(10)
add_task(timed_task2)
time.sleep(30)
remove_task(timed_task2)
time.sleep(20)
remove_task(timed_task)

```

用户也可以定制自己的Task类，需要在Task类中实现run()方法和meet_condition()方法，可参照ShellTask的实现
```
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

```
