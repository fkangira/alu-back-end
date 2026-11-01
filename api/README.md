# API

Four standalone Python scripts read employee TODO data from
[JSONPlaceholder](https://jsonplaceholder.typicode.com/). Only the standard
library is needed. The source uses syntax compatible with Python 3.4.3.

Run from this directory:

```sh
python3 0-gather_data_from_an_API.py 2
python3 1-export_to_CSV.py 2
python3 2-export_to_JSON.py 2
python3 3-dictionary_of_list_of_dictionaries.py
```

On Windows, replace `python3` with `python`.

| Script | Result |
| --- | --- |
| `0-gather_data_from_an_API.py` | Employee name, completion count, and completed titles. Each title starts with a tab and a space. |
| `1-export_to_CSV.py` | `USER_ID.csv`: all tasks, no header, all fields quoted. Field order: user ID, username, completion status, title. |
| `2-export_to_JSON.py` | `USER_ID.json`: a user ID mapped to tasks with `task`, `completed`, and `username` fields. |
| `3-dictionary_of_list_of_dictionaries.py` | `todo_all_employees.json`: every employee ID mapped to their tasks. No argument required. |

Exports are written to the current working directory, replacing an existing
file of the same name. CSV uses `True`/`False`; JSON uses booleans. Importing
the scripts does not make requests or write files. The first three scripts
expect a valid integer employee ID. Internet access is required.

The sample employee ID `2` is Ervin Howell (`Antonette`), with 8 completed
tasks out of 20.

Run the offline regression checks from the repository root:

```sh
python3 test_api.py -v
```

These checks cover exact progress formatting, CSV quoting and Unicode,
JSON values, grouping by employee, employees without tasks, and safe imports.

## Learning notes

- Python suits structured API data and serialization. Shell scripts suit
  command orchestration and simple text pipelines.
- An API defines how software components communicate. REST APIs expose
  resources over HTTP using methods such as GET, POST, PUT, PATCH, and DELETE.
- Microservices are independently deployable services communicating through
  interfaces such as APIs.
- CSV stores tabular rows and fields. JSON represents objects, arrays,
  strings, numbers, booleans, and null.
- Python modules, packages, variables, and functions generally use lowercase
  names with underscores. Classes use CapWords (PascalCase); constants use
  UPPER_CASE_WITH_UNDERSCORES.
- `dict.get(key)` returns a value or a default when a key is absent.
- The `__main__` guard prevents script execution when a module is imported.
