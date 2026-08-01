# Python CLI Application - Quick Overview

## Architecture

The Python CLI application is organized into 3 files in the `src/` directory:

### 1. db.py (12 lines)
- `connect()` - Establishes connection to PostgreSQL database
- Simple wrapper for psycopg2 connection management

### 2. queries.py (132 lines)
Contains 6 functions for database operations:

**view_books(conn)**
- Query: Selects available books with title, author, and available_copies
- Returns: List of tuples with book information

**active_loans(conn)**
- Query: Multi-table JOIN across Loan, Member, and Book tables
- Returns: List of active loans with member names, book titles, and due dates

**unpaid_fines(conn)**
- Query: JOIN + GROUP BY to calculate unpaid fines per member
- Returns: List of members with total amount owed

**add_book(conn, title, author, category, total_copies)**
- Inserts new book into Book table with available_copies = total_copies
- Includes input validation before database access

**available_books_with_ids(conn)**
- Similar to view_books but includes book_id for user selection

**loan_book(conn, member_id, book_id, staff_id, due_date)**
- Most complex function with transaction management
- First confirms book has available copies using FOR UPDATE lock
- Then inserts new loan record
- Then decrements available_copies in same transaction
- Commits only if all operations succeed
- Rolls back on any error to maintain data integrity

### 3. main.py (159 lines)
- **menu()** - Displays user options (1-5)
- **header()** - Formats section headers
- **handle_add_book()** - Handles adding new books with validation
- **handle_view_books()** - Displays available books
- **handle_active_loans()** - Shows active loans
- **handle_loan_book()** - Handles book borrowing with comprehensive validation
- **main()** - Main loop with connection handling and error management

## Key Features

1. **Input Validation**
   - Checks that all IDs are positive integers
   - Validates required fields (title, author, copies)
   - Prevents invalid database entries

2. **Transaction Management**
   - Uses database transactions for critical operations
   - Commits only if all operations succeed
   - Rolls back on errors to maintain consistency

3. **Error Handling**
   - Catches psycopg2 database errors
   - Handles invalid input gracefully
   - Provides clear error messages to user

4. **Race Condition Prevention**
   - Uses FOR UPDATE lock in loan_book() to prevent concurrent borrows of last copy

5. **User Experience**
   - Formatted output with visual indicators (✓ for success, ✗ for errors)
   - Clear section headers and separators
   - Helpful prompts and instructions

## Usage

Run from terminal:
```bash
python src/main.py
```

User can then:
1. Add new books
2. View available books
3. View active loans
4. Loan a book (requires selecting book ID, member ID, staff ID, and due date)
5. Exit the application

All database operations are handled through the queries.py functions, keeping main.py clean and focused on user interaction.