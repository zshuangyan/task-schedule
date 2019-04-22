from unittest import TestCase, TestSuite
from task_schedule.schedule_task import add_task, remove_task, clear_task, TaskExistError, TaskNotExistError
from task_schedule.task import ShellTask
from task_schedule.timed_task import TaskOption
import time


class TestScheduleTask(TestCase):
    def tearDown(self):
        print("清理所有任务")
        clear_task()

    def test_schedule_task_not_exist(self):
        opts = TaskOption(period=10)
        task = ShellTask("echo \"task1\"")
        print("启动task1")
        add_task("task1", task, opts)
        time.sleep(10)

        opts = TaskOption(period=5)
        print("启动task2")
        task = ShellTask("echo \"task2\"")
        add_task("task2", task, opts)
        time.sleep(15)

    def test_schedule_task_already_exist(self):
        opts = TaskOption(period=10)
        task = ShellTask("echo \"task1\"")
        print("启动task1")
        add_task("task1", task, opts)
        time.sleep(10)

        opts = TaskOption(period=5)
        print("启动task1")
        try:
            add_task("task1", task, opts)
        except Exception as e:
            self.assertEqual(type(e), TaskExistError)
        else:
            self.fail("TaskExistError not raised")

    def test_stop_task_not_exist(self):
        try:
            remove_task("task1")
        except Exception as e:
            self.assertEqual(type(e), TaskNotExistError)
        else:
            self.fail("TaskNotExistError not raised")

    def test_stop_task_already_exist(self):
        opts = TaskOption(period=10)
        task = ShellTask("echo \"task1\"")
        print("启动task1")
        add_task("task1", task, opts)
        time.sleep(10)

        remove_task("task1")


suit = TestSuite()
suit.addTest(test=TestScheduleTask("test_schedule_task_not_exist"))
suit.addTest(test=TestScheduleTask("test_schedule_task_already_exist"))
suit.addTest(test=TestScheduleTask("test_stop_task_not_exist"))
suit.addTest(test=TestScheduleTask("test_stop_task_already_exist"))


