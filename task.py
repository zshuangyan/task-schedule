from abc import ABCMeta, abstractmethod

class Task(metaclass=ABCMeta):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def meet_condition(self, *args, **kwargs):
        pass
