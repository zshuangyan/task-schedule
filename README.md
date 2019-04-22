# task-schedule
基于多线程和事件实现的定时任务

支持Python版本：3.5+

安装:
python setup.py install

接口-添加任务：
add_task(name, task, opts)

接口-删除任务:
remove_task(name)

接口-清理所有任务:
clear_task()

系统已实现了基于Shell命令执行的任务, 使用方法示例：  
```
from task_schedule import ShellTask, TaskOption, add_task, remove_task, clear_task
from datetime import datetime, timedelta

task = ShellTask("echo task1")
add_task("task1", task, TaskOption(start="2019-04-22 15:40:00", period=10))

task2 = ShellTask("echo task2")
add_task("task2", task2, TaskOption(start=datetime.now(), end="2019-04-22 15:48:00", period=5))

remove_task("task1")

task3 = ShellTask("echo task3")
add_task("task3", task3, TaskOption(period=timedelta(seconds=10)))

clear_task()
```

用户也可以定制自己的Task类，需要在Task类中实现run()方法，可参照ShellTask的实现
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
```
