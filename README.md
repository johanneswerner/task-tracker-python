# TASK TRACKER

## Introduction

Task Tracker is a simple CLI tool for managing tasks. This is a project from roadmaps.sh.

Link to the project: https://roadmap.sh/projects/task-tracker

## Features

- Add new tasks
- List all tasks
- Mark tasks as completed and in-progress
- Delete tasks
- Save tasks to a JSON file and load tasks from it

## Installation

To run task tracker, only Python and (and pytest for running the tests) is needed. Tested with Python v. 3.12.4.

## Usage

To use Task Tracker, run the `task_cli.py` script with the appropriate commands:

### Add a new task
Add a new task to the task list.

```sh
python task_cli.py add "Your new task"
```

### List all tasks

List all tasks with their status (completed or in-progress).

```sh
python task_cli.py list
```

`todo`, `in_progress`, `done` show a subset of the tasks list with their corresponding status.

### Mark a task as completed

Mark a task as completed by providing its task ID.

```sh
python task_cli.py mark-done 1
```

`mark-in-progress` marks a task as in progress. `todo` is only assigned for newly added tasks.

### Delete a task

Delete a task by providing its task ID.

```sh
python task_cli.py delete 1
```

## Contributing

For any suggestions and contributions, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
