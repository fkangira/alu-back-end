#!/usr/bin/python3
"""Display an employee's completed TODO tasks from JSONPlaceholder."""

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

    completed = [task for task in tasks if task.get("completed")]
    print("Employee {} is done with tasks({}/{}):".format(
        employee.get("name"), len(completed), len(tasks)))
    for task in completed:
        print("\t {}".format(task.get("title")))
