import psycopg2
from db import connect
from queries import view_books, active_loans, add_book, available_books_with_ids, loan_book

# formatting helpers

LINE  = "─" * 58
TITLE = "  Library Management System  ·  CS4092 Final Project"


def header(text):
    print(f"\n{LINE}")
    print(f"  {text}")
    print(LINE)


def menu():
    print(f"\n{'─' * 58}")
    print(f"  {TITLE}")
    print(f"{'─' * 58}")

    print("  1.  Add a new book")
    print("  2.  View available books")
    print("  3.  View active loans")
    print("  4.  Loan a book")
    print("  5.  Exit")

    print(f"{'─' * 58}")


# functions to handle user requests

def handle_view_books(conn):

    header("Available Books")
    rows = view_books(conn)

    if not rows:
        print("  No books currently available.")
        return
    
    print("  " + "Title".ljust(35) + "Author".ljust(22) + "Copies")
    for title, author, copies in rows:
        print("  " + title.ljust(35) + author.ljust(22) + str(copies))


def handle_active_loans(conn):

    header("Active Loans  (not yet returned)")
    rows = active_loans(conn)

    if not rows:
        print("  No active loans.")
        return

    print("  " + "Member".ljust(22) + "Book".ljust(30) + "Due Date")

    for first, last, title, due in rows:
        member = f"{first} {last}"
        print("  " + member.ljust(22) + title.ljust(30) + str(due))


def handle_loan_book(conn):

    header("Loan a Book")

    # Show available books so the user can see their IDs.
    books = available_books_with_ids(conn)
    if not books:
        print("  No books currently available to loan.")
        return

    print("  " + "ID".ljust(6) + "Title".ljust(35) + "Copies")
    for book_id, title, copies in books:
        print("  " + str(book_id).ljust(6) + title.ljust(35) + str(copies))
    print()

    book_id_input   = input("  Book ID:       ").strip()
    member_id_input = input("  Member ID:     ").strip()
    staff_id_input  = input("  Staff ID:      ").strip()
    due_date_input  = input("  Due date (YYYY-MM-DD): ").strip()

    # Validate that all IDs are positive integers before hitting the database.
    for label, value in [("Book ID", book_id_input), ("Member ID", member_id_input), ("Staff ID", staff_id_input)]:
        if not value.isdigit() or int(value) <= 0:
            print(f"\n  ✗  {label} must be a positive whole number.")
            return

    try:
        loan_book(
            conn,
            member_id = int(member_id_input),
            book_id   = int(book_id_input),
            staff_id  = int(staff_id_input),
            due_date  = due_date_input,
        )
        print("\n  ✓  Loan recorded successfully.")
    
    except ValueError as e:
        print(f"\n  ✗  {e}")
    
    except psycopg2.Error as e:
        conn.rollback()
        print(f"\n  ✗  Database error: {e.pgerror or e}")


def handle_add_book(conn):
    header("Add a New Book")
    title        = input("  Title:         ").strip()
    author       = input("  Author:        ").strip()
    category     = input("  Category:      ").strip()
    copies_input = input("  Total copies:  ").strip()

    # Basic validation before touching the database.
    if not title or not author or not copies_input:
        print("\n  ✗  Title, author, and total copies are required.")
        return

    if not copies_input.isdigit() or int(copies_input) <= 0:
        print("\n  ✗  Total copies must be a positive whole number.")
        return

    try:
        add_book(conn, title, author, category or None, int(copies_input))
        print(f"\n  ✓  '{title}' added successfully.")
    except psycopg2.Error as e:
        # Roll back the failed transaction so the connection stays usable.
        conn.rollback()
        print(f"\n  ✗  Database error: {e.pgerror or e}")


# main loop

def main():
    try:
        conn = connect()
    except psycopg2.OperationalError as e:
        print(f"Could not connect to library_db: {e}")
        return

    while True:
        menu()
        choice = input("  Select an option: ").strip()

        if   choice == "1": handle_add_book(conn)
        elif choice == "2": handle_view_books(conn)
        elif choice == "3": handle_active_loans(conn)
        elif choice == "4": handle_loan_book(conn)
        elif choice == "5":
            print("\n  Goodbye.\n")
            break
        else:
            print("\n  ✗  Invalid option. Enter a number from 1 to 5.")

    conn.close()


if __name__ == "__main__":
    main()
