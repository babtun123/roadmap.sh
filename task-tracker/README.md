# Task Tracker CLI

A simple command-line tool for managing tasks, with persistent storage in a local JSON file. Built as a learning project using only the Python standard library.

## Features

- Add, update, and delete tasks
- Mark tasks as in-progress or done
- List all tasks, or filter by status (`todo`, `in-progress`, `done`)
- Automatic timestamps for creation and last update
- Persistent storage in a human-readable JSON file

## Requirements

- Python 3.9 or later
- No external dependencies (standard library only)

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/babtun123/roadmap.sh.git
cd roadmap.sh/task-tracker
```

No further setup is needed.

## Usage

All commands follow the pattern:

```bash
python3 task_cli.py <command> [arguments...]
```

Running the script with no arguments, or with an unknown command, prints a usage summary.

### Add a task

Wrap multi-word descriptions in quotes.

```bash
python3 task_cli.py add "Buy groceries"
```

### Update a task's description

```bash
python3 task_cli.py update 1 "Buy groceries and cook dinner"
```

### Delete a task

```bash
python3 task_cli.py delete 1
```

### Mark a task as in-progress or done

```bash
python3 task_cli.py mark-in-progress 1
python3 task_cli.py mark-done 1
```

### List tasks

```bash
python3 task_cli.py list                 # all tasks
python3 task_cli.py list todo            # only unstarted tasks
python3 task_cli.py list in-progress     # only in-progress tasks
python3 task_cli.py list done            # only completed tasks
```

## Data Storage

Tasks are stored in a file named `tasks.json` in the current working directory. The file is created automatically on first use.

Each task has the following fields:

- `id` — an integer, unique within the file
- `description` — a string
- `status` — one of `todo`, `in-progress`, `done`
- `createdAt` — an ISO 8601 timestamp
- `updatedAt` — an ISO 8601 timestamp

Example `tasks.json`:

```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "status": "done",
    "createdAt": "2026-04-22T14:06:31.270704",
    "updatedAt": "2026-04-22T14:26:54.209404"
  },
  {
    "id": 2,
    "description": "Call mom",
    "status": "todo",
    "createdAt": "2026-04-22T14:07:21.746085",
    "updatedAt": "2026-04-22T14:07:21.746085"
  }
]
```

## Notes and Limitations

- **Per-directory storage.** Because `tasks.json` lives in the current working directory, running the tool from a different folder gives you a different task list. Be consistent about where you run it from.
- **Timestamps use local time**, not UTC. If you move the file between machines in different time zones, the timestamps will still be valid ISO 8601 but will reflect the time zone they were written in.
- **IDs are never reused.** Deleting a task does not free its ID; new tasks continue incrementing from the highest ID ever used.
- **Quoting matters.** `add Buy groceries` (no quotes) will fail because the shell splits it into two arguments. Always quote multi-word descriptions.
