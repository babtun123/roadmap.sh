"""Expense tracker cli"""

import argparse
import json
from datetime import datetime

EXPENSE_FILE = "expense.json"

def handle_add(descr, amount_fl):
    """add func"""
    expenses = load_expenses()
    if expenses:
        new_id = max(expense["id"] for expense in expenses) + 1
    else:
        new_id = 1

    now_as_string = _now()
    new_expense = {
        "id": new_id,
        "description": descr,
        "amount": amount_fl,
        "createdAt": now_as_string,
        "updatedAt": now_as_string
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")

def handle_update(upd_id, updt_desc, updt_amnt):
    """update func"""
    index, expenses = _find_expense(upd_id)
    if index is None:
        return

    if updt_desc is None and updt_amnt is None:
        print("No value was provided for description or amount to be updated.")
        return

    if updt_desc is not None:
        expenses[index]["description"] = updt_desc
    if updt_amnt is not None:
        expenses[index]["amount"] = updt_amnt
    expenses[index]["updatedAt"] = _now()

    expense_id = expenses[index]["id"]
    save_expenses(expenses)
    print(f"Successfully updated ID: {expense_id}")

def handle_delete(del_id):
    """delete func"""
    index, expenses = _find_expense(del_id)
    if index is None:
        return

    deleted_id = expenses[index]["id"]
    del expenses[index]
    save_expenses(expenses)
    print(f"Successfully deleted {deleted_id}")

def handle_list():
    """view func"""
    expenses = load_expenses()
    if not expenses:
        print("Error: No expenses exist yet. Add one with 'add'")
        return
    print("ID   Date    Description     Amount")
    for expense in expenses:
        print(f"{expense["id"]}  {expense["createdAt"][:10]}"
              f"    {expense["description"]}     ${expense["amount"]}"
        )

def handle_summary():
    """summary func"""

def _now():
    return datetime.now().isoformat()

def _find_expense(id_num):
    """Helper function that will search through
    the list of expenses and return the index of 
    of given id number.
    """
    expenses = load_expenses()
    if not expenses:
        print("Error: No expenses exist yet. Add one with add command")
        return None, None
    index = next((i for i, t in enumerate(expenses) if t["id"] == id_num), None)
    if index is None:
        print(f"Error: No task found with ID {id_num}")
        return None, None
    return index, expenses

def load_expenses():
    """Read expenses from the JSON file. Returns a list of expense dicts."""
    try:
        with open(EXPENSE_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            return loaded
    except FileNotFoundError:
        return []

def save_expenses(expense_list):
    """Write the given list of expenses to the JSON file."""
    with open(EXPENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(expense_list, f, indent=2)


def main():
    """Main func"""

    parser = argparse.ArgumentParser(description="Expense tracker cli application")
    subparsers = parser.add_subparsers(dest="command")

    # Add parser
    add_parser = subparsers.add_parser("add", help="add parser help")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True)

    # Update parser
    update_parser = subparsers.add_parser("update", help="update parser help")
    update_parser.add_argument("--id", type=int, required=True)
    update_parser.add_argument("--description", required=False)
    update_parser.add_argument("--amount", type=float, required=False)

    # Delete parser
    delete_parser = subparsers.add_parser("delete", help="delete parser help")
    delete_parser.add_argument("--id", type=int, required=True)

    #List parser
    list_parser = subparsers.add_parser("list", help="list parser help")
    _ = list_parser

    args = parser.parse_args()
    print()

    if args.command == "add":
        add_des, add_amount = args.description, args.amount
        handle_add(add_des, add_amount)
    elif args.command == "update":
        handle_update(args.id, args.description, args.amount)
    elif args.command == "delete":
        handle_delete(args.id)
    elif args.command == "list":
        handle_list()
    else:
        print(f"{args.command} not found")

if __name__ == "__main__":
    main()
