"""Tests for task-manager.py.

The file name has a hyphen, so I load it by path instead of
importing it by name. Loading it must not start the menu: the
loop sits under the main guard, and the first test would hang
or fail on input if that ever changed.
"""
import importlib.util
import pathlib
import subprocess
import sys
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).parent
SOURCE = HERE / "task-manager.py"

spec = importlib.util.spec_from_file_location("task_manager", SOURCE)
tm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tm)


def run_program(stdin_text):
    return subprocess.run(
        [sys.executable, str(SOURCE)],
        input=stdin_text, capture_output=True, text=True, timeout=15,
    )


class TaskClassTests(unittest.TestCase):
    def test_seed_style_strings_become_ints(self):
        t = tm.task("walk dog", "1", "2")
        self.assertEqual(t.Completed_Uncompleted, 1)
        self.assertEqual(t.Days, 2)

    def test_task_due_at_zero_and_negative(self):
        self.assertIn("due task", tm.task("a", 0, 0).task_due())
        self.assertIn("due task", tm.task("a", 0, -3).task_due())
        self.assertIn("not due", tm.task("a", 0, 5).task_due())

    def test_day_passed_decrements_and_has_a_space(self):
        t = tm.task("a", 0, 3)
        result = t.day_passed()
        self.assertEqual(t.Days, 2)
        self.assertTrue(result.endswith("now 2"), result)

    def test_remove_completed_mutates_the_callers_list(self):
        tasks = [tm.task("done", 1, 1), tm.task("open", 0, 4)]
        tm.removeCompleted(tasks)
        self.assertEqual([t.Task for t in tasks], ["open"])

    def test_first_and_random_on_empty_list_do_not_raise(self):
        tm.firstTask([])
        tm.randomTask([])


class MenuRunTests(unittest.TestCase):
    def test_quit_exits_zero(self):
        r = run_program("7\n")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Bye! Bye!", r.stdout)

    def test_eof_at_menu_exits_zero_without_traceback(self):
        r = run_program("")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Bye! Bye!", r.stdout)
        self.assertNotIn("Traceback", r.stderr)

    def test_bad_menu_input_returns_to_menu(self):
        r = run_program("abc\n3.5\n99\n7\n")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.count("Please enter a number from 1 to 7."), 3)

    def test_print_shows_both_seed_tasks(self):
        r = run_program("3\n7\n")
        self.assertIn("walk dog", r.stdout)
        self.assertIn("Eat tree", r.stdout)

    def test_complete_exact_name_marks_and_reports(self):
        r = run_program("2\nEat tree\n3\n7\n")
        self.assertIn("Marked completed: Eat tree", r.stdout)

    def test_complete_unknown_name_says_so(self):
        r = run_program("2\nnonsense\n7\n")
        self.assertEqual(r.returncode, 0)
        self.assertIn("No task named 'nonsense' found.", r.stdout)

    def test_add_then_print(self):
        r = run_program("1\nwrite tests\n4\n3\n7\n")
        self.assertIn("write tests", r.stdout)

    def test_add_rejects_text_days(self):
        r = run_program("1\nthing\nabc\n3\n7\n")
        self.assertIn("must be a whole number of days. Task not added.", r.stdout)
        self.assertNotIn("Your task is: thing", r.stdout)

    def test_add_rejects_negative_days(self):
        r = run_program("1\nthing\n-5\n3\n7\n")
        self.assertIn("cannot be negative. Task not added.", r.stdout)
        self.assertNotIn("Your task is: thing", r.stdout)

    def test_add_rejects_blank_description(self):
        r = run_program("1\n\n5\n3\n7\n")
        self.assertIn("description cannot be blank. Task not added.", r.stdout)

    def test_remove_then_print_keeps_only_open_tasks(self):
        r = run_program("4\n3\n7\n")
        after = r.stdout.split("Loading Task Information:")[-1]
        self.assertIn("Eat tree", after)
        self.assertNotIn("walk dog", after)

    def test_next_picks_fewest_days_as_numbers(self):
        r = run_program("1\nfar task\n100\n6\n7\n")
        section = r.stdout.split("Locating the first task")[-1]
        self.assertIn("walk dog", section)
        self.assertNotIn("far task", section.split("Welcome")[0])

    def test_empty_list_next_and_random_do_not_crash(self):
        r = run_program("2\nEat tree\n4\n5\n6\n7\n")
        self.assertEqual(r.returncode, 0)
        self.assertIn("There are no tasks to choose from.", r.stdout)
        self.assertIn("There are no tasks.", r.stdout)

    def test_keyboard_interrupt_quits_without_traceback(self):
        answers = mock.Mock(side_effect=KeyboardInterrupt)
        with mock.patch("builtins.input", answers):
            with mock.patch("sys.stdout"):
                tm.main()
