"""Expense tracker cli"""

import argparse

def print_usage():
    """Menu options for user"""
    print("Usage: expense_cli.py <command> [args...]")
    print()

def main():
    """Main func"""

    parser = argparse.ArgumentParser(description="Expense tracker cli application")
    subparsers = parser.add_subparsers(dest="command")

    # Add parser
    add_parser = subparsers.add_parser("add", help="add parser help")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True)

    # Delete parser
    delete_parser = subparsers.add_parser("delete", help="delete parser help")
    delete_parser.add_argument("--delete", required=True)

    args = parser.parse_args()

    print(args)
    print()

    if args.command == "add":
        print(f"Adding {args.description} and {args.amount}")


if __name__ == "__main__":
    main()
