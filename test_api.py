#!/usr/bin/python3
"""Verify API scripts offline with deterministic employee and task data."""

import contextlib
import csv
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api")
SCRIPTS = ["0-gather_data_from_an_API.py", "1-export_to_CSV.py",
           "2-export_to_JSON.py", "3-dictionary_of_list_of_dictionaries.py"]
USERS = [{"id": 2, "name": "Ervin Howell", "username": "Antonette"},
         {"id": 3, "name": "Other", "username": "OtherUser"},
         {"id": 4, "name": "Empty", "username": "NoTasks"}]
TASKS = [{"userId": 2, "title": 'A, "quoted" task', "completed": True},
         {"userId": 2, "title": "caf\u00e9", "completed": False},
         {"userId": 3, "title": "Other task", "completed": True}]


def fake_urlopen(url):
    """Return a mock HTTP response for the requested resource."""
    if url.endswith("/users"):
        data = USERS
    elif url.endswith("/todos"):
        data = TASKS
    elif "/users/" in url:
        employee_id = int(url.rsplit("/", 1)[1])
        data = next(user for user in USERS if user.get("id") == employee_id)
    else:
        employee_id = int(url.rsplit("=", 1)[1])
        data = [task for task in TASKS if task.get("userId") == employee_id]
    return io.BytesIO(json.dumps(data).encode("utf-8"))


class ApiTests(unittest.TestCase):
    """Check observable behavior without accessing the public API."""

    def setUp(self):
        """Isolate generated exports in a temporary directory."""
        self.original = os.getcwd()
        self.temp = tempfile.TemporaryDirectory()
        os.chdir(self.temp.name)

    def tearDown(self):
        """Restore the original directory and remove test exports."""
        os.chdir(self.original)
        self.temp.cleanup()

    def run_script(self, index, employee_id=2):
        """Execute a script with mocked HTTP and captured standard output."""
        script = os.path.join(ROOT, SCRIPTS[index])
        output = io.StringIO()
        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            with patch.object(sys, "argv", [script, str(employee_id)]):
                with contextlib.redirect_stdout(output):
                    runpy.run_path(script, run_name="__main__")
        return output.getvalue()

    def test_progress_format(self):
        """Use the employee's name and exact title indentation."""
        self.assertEqual(self.run_script(0),
                         "Employee Ervin Howell is done with tasks(1/2):\n"
                         '\t A, "quoted" task\n')

    def test_progress_without_tasks(self):
        """An employee with no tasks has a zero completion count."""
        self.assertEqual(self.run_script(0, 4),
                         "Employee Empty is done with tasks(0/0):\n")

    def test_csv(self):
        """Export every task with quoted fields and escaped titles."""
        self.assertEqual(self.run_script(1), "")
        with open("2.csv", encoding="utf-8", newline="") as stream:
            self.assertEqual(list(csv.reader(stream)), [
                ["2", "Antonette", "True", 'A, "quoted" task'],
                ["2", "Antonette", "False", "caf\u00e9"]])
        with open("2.csv", encoding="utf-8") as stream:
            self.assertEqual(stream.read(),
                             '"2","Antonette","True",'
                             '"A, ""quoted"" task"\n'
                             '"2","Antonette","False","caf\u00e9"\n')

    def test_json(self):
        """Preserve boolean status and include both completed states."""
        self.assertEqual(self.run_script(2), "")
        with open("2.json", encoding="utf-8") as stream:
            self.assertEqual(json.load(stream), {"2": [
                {"task": task.get("title"),
                 "completed": task.get("completed"), "username": "Antonette"}
                for task in TASKS if task.get("userId") == 2]})

    def test_json_without_tasks(self):
        """Keep an empty employee's key in the export."""
        self.run_script(2, 4)
        with open("4.json", encoding="utf-8") as stream:
            self.assertEqual(json.load(stream), {"4": []})

    def test_all_employees(self):
        """Group all tasks by owner, including employees without tasks."""
        self.assertEqual(self.run_script(3), "")
        with open("todo_all_employees.json", encoding="utf-8") as stream:
            data = json.load(stream)
        self.assertEqual(set(data), {"2", "3", "4"})
        for user in USERS:
            expected = [{"username": user.get("username"),
                         "task": task.get("title"),
                         "completed": task.get("completed")}
                        for task in TASKS
                        if task.get("userId") == user.get("id")]
            self.assertEqual(data.get(str(user.get("id"))), expected)

    def test_imports_are_safe(self):
        """Importing any script must not access the network or write files."""
        with patch("urllib.request.urlopen") as request:
            for script in SCRIPTS:
                module = runpy.run_path(os.path.join(ROOT, script),
                                        run_name="import_check")
                self.assertTrue(module.get("__doc__"))
            self.assertEqual(request.call_count, 0)
        self.assertEqual(os.listdir(self.temp.name), [])


if __name__ == "__main__":
    unittest.main()
