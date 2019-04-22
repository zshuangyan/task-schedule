from task_schedule.task import Task
from unittest import TestCase


class TestTask(TestCase):
    def test_task_without_run(self):
        class InheritTask(Task):
            def __init__(self):
                pass

        try:
            InheritTask()
        except Exception as e:
            self.assertEqual(type(e), TypeError)
        else:
            self.fail("TypeError not raised")
