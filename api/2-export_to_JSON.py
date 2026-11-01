#!/usr/bin/python3
"""Export all TODO tasks for one employee to a JSON file."""

import json
import sys
import urllib.request


if __name__ == "__main__":
    employee_id = int(sys.argv[1])
    base_url = "https://jsonplaceholder.typicode.com"
    with urllib.request.urlopen(
            "{}/users/{}".format(base_url, employee_id)) as response:
        employee = json.loads(response.read().decode("utf-8"))
    with urllib.request.urlopen(
            "{}/todos?userId={}".format(base_url, employee_id)) as response:
        tasks = json.loads(response.read().decode("utf-8"))

    data = {str(employee_id): [
        {"task": task.get("title"), "completed": task.get("completed"),
         "username": employee.get("username")} for task in tasks
    ]}
    with open("{}.json".format(employee_id), "w", encoding="utf-8") as out:
        json.dump(data, out)
