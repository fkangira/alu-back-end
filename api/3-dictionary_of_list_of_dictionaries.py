#!/usr/bin/python3
"""Export every employee's TODO tasks to todo_all_employees.json."""

import json
import urllib.request


if __name__ == "__main__":
    base_url = "https://jsonplaceholder.typicode.com"
    with urllib.request.urlopen(base_url + "/users") as response:
        employees = json.loads(response.read().decode("utf-8"))
    with urllib.request.urlopen(base_url + "/todos") as response:
        tasks = json.loads(response.read().decode("utf-8"))

    data = {}
    for employee in employees:
        employee_id = employee.get("id")
        data[str(employee_id)] = [
            {"username": employee.get("username"),
             "task": task.get("title"), "completed": task.get("completed")}
            for task in tasks if task.get("userId") == employee_id
        ]

    with open("todo_all_employees.json", "w", encoding="utf-8") as out:
        json.dump(data, out)
