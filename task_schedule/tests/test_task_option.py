from unittest import TestCase
from task_schedule.timed_task import TaskOption, TimeFormatError
from datetime import datetime, timedelta


class TestScheduleTask(TestCase):
    def test_task_start_time_in_correct_format(self):
        TaskOption(start="2019-04-22 15:00:00", period=5)
        TaskOption(start=datetime.now(), period=10)

    def test_task_start_time_in_wrong_format(self):
        try:
            TaskOption(start="19-04-22 15:02:00", period=5)
        except Exception as e:
            self.assertEqual(type(e), TimeFormatError)
        else:
            self.fail("TimeFormatError should raised")

    def test_task_end_time_in_correct_format(self):
        TaskOption(end="2019-04-22 15:00:00", period=5)
        TaskOption(end=datetime.now(), period=10)

    def test_task_end_time_in_wrong_format(self):
        try:
            TaskOption(end="19-04-22 15:02:00", period=5)
        except Exception as e:
            self.assertEqual(type(e), TimeFormatError)
        else:
            self.fail("TimeFormatError should raised")

    def test_task_period_in_correct_format(self):
        TaskOption(period=5)
        task_option = TaskOption(period=timedelta(seconds=10))
        self.assertEqual(task_option.period, 10)

    def test_task_period_in_wrong_format(self):
        try:
            TaskOption(period=0)
        except Exception as e:
            self.assertEqual(type(e), TimeFormatError)
        else:
            self.fail("TimedFormatError should raised")