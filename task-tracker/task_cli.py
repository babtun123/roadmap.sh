"""Task cli app"""

import sys
import json
from datetime import datetime

TASKS_FILE = "tasks.json"
VALID_STATUSES = ("todo", "in-progress", "done")

def handle_add(args):
    """Add a new task to the JSON file.

    args should contain a single element: the task description.
    Prints a success message with the new task's ID, or an error
    if no description was provided.
    """
    if len(args) < 1:
        print("Error: 'add' requires a description")
        return
    description = args[0]
    if len(args) > 1:
        print("Error: 'add' takes exactly one argument (did you forget quotes?)")
        return
    tasks = load_tasks()

    if tasks:
        new_id = max(task["id"] for task in tasks) + 1
    else:
        new_id = 1

    now_as_string = _now()

    new_task = {
        "id": new_id, 
        "description": description, 
        "status": VALID_STATUSES[0],
        "createdAt": now_as_string, 
        "updatedAt": now_as_string,
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def handle_list(args):
    """list tasks, optionally filtered by status

    with no arguements, print all tasks
    with one argument, ('done', 'todo', or 'in-progress)
    print only tasks with that status
    """
    if len(args) > 1:
        print("Error: list takes at most one argument (did you mean 'in-progress'?)")
        return

    tasks = load_tasks()
    if not tasks:
        print("Error: No tasks found")
        return

    # Determine which tasks to show
    if len(args) == 0:
        task_to_show = tasks
    else:
        filter_name = args[0]
        if filter_name not in VALID_STATUSES:
            print(f"Error: '{filter_name}' is not a valid status")
            return
        task_to_show = [t for t in tasks if t["status"] == filter_name]

    if not task_to_show:
        print(f"Error: No tasks with status '{args[0]}'")
        return

    for task in task_to_show:
        print(
            f"id: {task['id']} "
            f"description: {task['description']} "
            f"status: {task['status']}"
        )

def _find_task(args):
    """Parse a task ID from args, load tasks, and find the matching task.

    Used by update, delete, mark-in-progress, and mark-done — all of which
    need to locate an existing task by ID before doing their own thing.

    On success, returns (tasks_list, index).
    On any failure (missing arg, non-numeric ID, empty file, no match),
    prints an error and returns (None, None). The caller should check
    for None and return early.
    """
    if not args:
        print("Error: missing Id number")
        return None, None

    try:
        task_id = int(args[0])
    except ValueError:
        print(f"Error: '{args[0]}' is not a valid task ID (expected a number)")
        return None, None

    tasks = load_tasks()
    if not tasks:
        print("No tasks exist yet. Add one with add 'description'")
        return None, None

    index = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
    if index is None:
        print(f"Error: No task found with ID {task_id}")
        return None, None

    return tasks, index

def _now():
    return datetime.now().isoformat()

def handle_update(args):
    """used to update a task"""
    if len(args) != 2:
        print("Error: 'update' requires exactly two arguments: an ID and a new description")
        return
    tasks, index = _find_task(args)
    if index is None:
        return

    current_description = tasks[index]["description"]
    tasks[index]["description"] = args[1]
    tasks[index]["updatedAt"] = _now()

    task_id = tasks[index]["id"]
    save_tasks(tasks)
    print(f"Task {task_id} description changed from '{current_description}' to '{args[1]}'")


def handle_delete(args):
    """Delete a task by its ID."""
    tasks, index = _find_task(args)
    if index is None:
        return

    deleted_id = tasks[index]["id"]
    del tasks[index]
    save_tasks(tasks)
    print(f"Task {deleted_id} deleted successfully")

def _mark_status(args, new_status):
    """helper function for handle_mark_in_progress and handle_mark_done"""
    tasks, index = _find_task(args)
    if index is None:
        return

    task = tasks[index]
    task["status"] = new_status
    task["updatedAt"] = _now()
    save_tasks(tasks)
    print(f"Task {task['id']} marked as {new_status}")

def handle_mark_in_progress(args):
    """used to mark a task as in-progress"""
    _mark_status(args, VALID_STATUSES[1])

def handle_mark_done(args):
    """used to mark a task as done"""
    _mark_status(args, VALID_STATUSES[2])


# I'm using a dictionary to map each user task input
# to the functionality. Why not an if statement?
# Turns out that functions are first class object in
# python and I can set a variable to a function
# without calling the function.
# When the the input is add, I map it to the
# corresponding function
commands = {
    "add": handle_add,
    "list": handle_list,
    "update": handle_update,
    "delete": handle_delete,
    "mark-in-progress": handle_mark_in_progress,
    "mark-done": handle_mark_done
}

def load_tasks():
    """Read tasks from the JSON file. Returns a list of task dicts."""
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            return loaded
    except FileNotFoundError:
        return []

def save_tasks(tasks_list):
    """Write the given list of tasks to the JSON file."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks_list, f, indent=2)

def print_usage():
    """Menu options for user"""
    print("Usage: task_cli.py <command> [args...]")
    print()
    print("Commands:")
    print("  add <description>                 Add a new task")
    print("  list [status]                     List tasks (optionally filter by status)")
    print("  update <id> <description>         Update a task's description")
    print("  delete <id>                       Delete a task")
    print("  mark-in-progress <id>             Mark a task as in-progress")
    print("  mark-done <id>                    Mark a task as done")
    print()
    print("Statuses for 'list': todo, in-progress, done")

def main():
    """main func"""
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    if command in commands:
        commands[command](args)
    else:
        print(f"unknown command {command}")
        print()
        print_usage()

if __name__ == "__main__":
    main()
