from db import connect
import psycopg2


def view_books(conn):
    """
    SELECT title, author, available_copies FROM Book WHERE available_copies > 0
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT title, author, available_copies
        FROM Book
        WHERE available_copies > 0
        ORDER BY title;
    """)

    rows = cur.fetchall()
    cur.close()
    
    return rows


def active_loans(conn):
    """
    Multi-table JOIN across Loan, Member, Book.
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT m.first_name, m.last_name, b.title, l.due_date
        FROM Loan l
        JOIN Member m ON l.member_id = m.member_id
        JOIN Book   b ON l.book_id   = b.book_id
        WHERE l.return_date IS NULL
        ORDER BY l.due_date;
    """)

    rows = cur.fetchall()
    cur.close()
    return rows


def unpaid_fines(conn):
    """
    JOIN + GROUP BY to sum unpaid fines per member.
    Mirrors sql/unpaid_fine_by_member.sql
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT m.first_name, m.last_name, SUM(f.amount) AS total_owed
        FROM Fine f
        JOIN Loan   l ON f.loan_id   = l.loan_id
        JOIN Member m ON l.member_id = m.member_id
        WHERE f.paid = FALSE
        GROUP BY m.first_name, m.last_name
        ORDER BY total_owed DESC;
    """)

    rows = cur.fetchall()
    cur.close()
    return rows


def add_book(conn, title, author, category, total_copies):
    """
    INSERT a new book.
    """
    cur = conn.cursor()
    # %s are placeholders; psycopg2 substitutes the tuple safely at execute time.
    cur.execute("""
        INSERT INTO Book (title, author, category, total_copies, available_copies)
        VALUES (%s, %s, %s, %s, %s);
    """, (title, author, category, total_copies, total_copies))
    
    conn.commit()
    cur.close()


def available_books_with_ids(conn):
    """
    Like view_books but includes book_id so the loan handler can display IDs
    for the user to pick from.
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT book_id, title, available_copies
        FROM Book
        WHERE available_copies > 0
        ORDER BY title;
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def loan_book(conn, member_id, book_id, staff_id, due_date):
    """
    Record a new loan and decrement available_copies on the Book row.
    Both statements run inside the same transaction: if either fails,
    neither change is committed, keeping the database consistent.
    """
    cur = conn.cursor()

    # First, confirm the book still has copies available.
    # FOR UPDATE locks that row until we commit, preventing a race condition
    # if two people tried to borrow the last copy at the same time.
    cur.execute("""
        SELECT available_copies FROM Book WHERE book_id = %s FOR UPDATE;
    """, (book_id,))

    result = cur.fetchone()
    if result is None:
        cur.close()
        raise ValueError(f"No book found with ID {book_id}.")
    
    if result[0] <= 0:
        cur.close()
        raise ValueError("That book has no available copies.")

    # Insert the loan record. borrow_date defaults to CURRENT_DATE in the schema.
    cur.execute("""
        INSERT INTO Loan (member_id, book_id, staff_id, due_date)
        VALUES (%s, %s, %s, %s);
    """, (member_id, book_id, staff_id, due_date))

    # Decrement the copy count to reflect the book being checked out.
    cur.execute("""
        UPDATE Book SET available_copies = available_copies - 1
        WHERE book_id = %s;
    """, (book_id,))

    conn.commit()
    cur.close()
