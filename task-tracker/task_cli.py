"""Task cli app"""

import sys
import json
from datetime import datetime

TASKS_FILE = "tasks.json"

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
        print("task is empty")
        new_id = 1

    now_as_string = datetime.now().isoformat()

    new_task = {
        "id": new_id, 
        "description": description, 
        "status": "todo",
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
        print("No tasks found")
        return

    # Determine which tasks to show
    if len(args) == 0:
        task_to_show = tasks
    else:
        filter_name = args[0]
        if filter_name not in ("done", "todo", "in-progress"):
            print(f"Error: '{filter_name}' is not a valid status")
            return
        task_to_show = [t for t in tasks if t["status"] == filter_name]

    # Handle the "nothing matches the filter" case
    if not task_to_show:
        print(f"No tasks with status '{args[0]}'")
        return

    # print tasks
    for task in task_to_show:
        print(
            f"id: {task['id']} "
            f"description: {task['description']} "
            f"status: {task['status']}"
        )

def handle_update(args):
    """used to update a task"""
    print(f"update called with args: {args}")

def handle_delete(args):
    """used to delete a tesk"""
    print(f"delete called with args: {args}")

def handle_mark_in_progress(args):
    """used to mark a task as in-progress"""
    print(f"mark-in-progress called with args: {args}")

def handle_mark_done(args):
    """used to mark a task as done"""
    print(f"mark-done called with args: {args}")


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

def main():
    """main func"""
    command = sys.argv[1]
    args = sys.argv[2:]

    if command in commands:
        commands[command](args)
    else:
        print(f"unknown command {command}")

if __name__ == "__main__":
    main()
