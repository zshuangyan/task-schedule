from abc import ABCMeta, abstractmethod
import subprocess
import shlex


class Task(metaclass=ABCMeta):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass


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
