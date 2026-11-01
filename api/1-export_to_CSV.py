#!/usr/bin/python3
"""Export all TODO tasks for one employee to a fully quoted CSV file."""

import csv
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

    with open("{}.csv".format(employee_id), "w", newline="",
              encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for task in tasks:
            writer.writerow([employee_id, employee.get("username"),
                             task.get("completed"), task.get("title")])
