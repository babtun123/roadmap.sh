"""Expense tracker cli"""

import argparse
import json
from datetime import datetime

EXPENSE_FILE = "expense.json"
BUDGET_FILE = "budget.json"

def handle_add(descr, amount_fl):
    """add func"""
    expenses = load_expenses()
    if expenses:
        new_id = max(expense["id"] for expense in expenses) + 1
    else:
        new_id = 1

    if amount_fl < 0:
        print("Error: Can't add a negative amount")
        return

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

    get_month_val = new_expense["createdAt"][5:7]
    month_total = _total_for_month(expenses, get_month_val)

    budgets = load_budgets()
    month_budget = budgets.get(get_month_val)
    if month_budget is not None and month_total > month_budget:
        print(f"Warning: {month_map[get_month_val]} spending is ${month_total},"
                f" exceeding budget of ${month_budget} by ${month_total - month_budget}"
        )

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
        if updt_amnt < 0:
            print("Error: Can't update with a negative amount")
            return
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

def handle_summary(month_val):
    """summary func"""
    expenses = load_expenses()
    if not expenses:
        print("Error: No expenses exist yet. Add one with add command")
        return

    if month_val is not None:
        month_val_string = str(month_val).zfill(2)
        if not _validate_month(month_val):
            print(f"Error: '{month_val}' is not a valid month (must be 1-12)")
            return
        expense_count = _total_for_month(expenses, month_val_string)
        month = month_map[month_val_string]
        print(f"Total expenses for {month}: ${expense_count}")
    else:
        expense_count = sum(e["amount"] for e in expenses)
        print(f"Total expenses: ${expense_count}")

def handle_budget(month_val, amount_val):
    """Handle budget file. Used to handle budget"""
    month_val_string = str(month_val).zfill(2)

    if amount_val < 0:
        print(f"Error: '{amount_val}' is not valid (must be a 0 or higher)")
        return
    if not _validate_month(month_val):
        print(f"Error: '{month_val}' is not a valid month (must be 1-12)")
        return

    budgets = load_budgets()
    budgets[month_val_string] = amount_val

    save_budgets(budgets)
    print(f"Budget for {month_map[month_val_string]} set to ${amount_val}")

def _total_for_month(expenses, month_str):
    """Helper func to calculate total expenses for a particular month"""
    return sum(e["amount"] for e in expenses if e["createdAt"][5:7] == month_str)

def _validate_month(month_val):
    """Return True if month_val is between 1 and 12, False otherwise."""
    return 1 <= month_val <= 12

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

def load_budgets():
    """Read budgets from the JSON file. Return an object of each month's budget"""
    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            return loaded
    except FileNotFoundError:
        return {}

def save_budgets(budget_dict):
    """Used to update the budget object"""
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budget_dict, f, indent=2)

month_map = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

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

    # List parser
    list_parser = subparsers.add_parser("list", help="list parser help")
    _ = list_parser

    # Summary parser
    summary_parser = subparsers.add_parser("summary", help="summary parser help")
    summary_parser.add_argument("--month", type=int, required=False)

    # Budget parser
    budget_parser = subparsers.add_parser("budget", help="budget parser help")
    budget_parser.add_argument("--month", type=int, required=True)
    budget_parser.add_argument("--amount", type=float, required=True)

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
    elif args.command == "summary":
        handle_summary(args.month)
    elif args.command == "budget":
        handle_budget(args.month, args.amount)
    else:
        print(f"{args.command} not found")

if __name__ == "__main__":
    main()
