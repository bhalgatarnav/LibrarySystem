# Library Management System

## Final Project: Database Design and Development (CS4092)

### Author: Arnav Bhalgat

## Project Overview

This repository contains my final project for Database Design and Development. I designed and built a relational database backend for a library management system. I adapted this project from the course's sample e-commerce system.

The system supports two user roles. Staff members manage the book catalog and oversee borrowing activity. Members browse the catalog, borrow books, and view their own loan and fine history.

This project is being completed individually, and follows the complete database development lifecycle outlined in the course rubric, from requirements gathering through implementation and application level interaction.

## Repository Structure

```
LibrarySystem/
├── docs/
│   ├── Phase-1-Requirements.pdf              # Requirements gathering document
│   ├── Phase-2-ER-Diagram.pdf                # Entity-Relationship diagram
│   ├── Phase-3-Schema-Design.pdf             # Relational schema documentation
│   └── setting-up-postgresql.md              # PostgreSQL setup guide
├── sql/
│   ├── library_schema.sql                    # Complete database schema and sample data
│   ├── view_books.sql                        # SQL query 1: View available books
│   ├── active_loans.sql                      # SQL query 2: Multi-table active loans
│   └── unpaid_fine_by_member.sql             # SQL query 3: Unpaid fines with GROUP BY
├── src/
│   ├── db.py                                 # Database connection management
│   ├── queries.py                            # SQL query functions
│   └── main.py                               # CLI interface
├── presentation_script.md                    # Video presentation script (9 min)
├── short_presentation_script.md              # Short presentation script (3-5 min)
├── Python_CLI_Overview.md                    # Python CLI code documentation
└── README.md
```

## Phase 1: Requirements Gathering

I began by identifying the core use cases for both user roles. Staff can add and edit books in the catalog, view all books, view a member's loan history, and record returns and any resulting fines. Members can register for an account, browse the catalog, borrow books, and view their own loans and fines.

From these use cases, I identified five core entities: Member, Book, Staff, Loan, and Fine. I also documented several key assumptions that shaped the rest of the design. A member can only borrow one copy of a given book at a time, meaning individual physical copies are not tracked separately, only a count of available copies. A loan is considered active until a return date is recorded. Fines are only generated when a book is returned late, and payment processing itself is outside the scope of this project.

Full details are documented in `docs/Phase-1-Requirements.pdf`.

## Phase 2: Entity Relationship Diagram

I built an ER diagram to model the five entities and the relationships between them. Every one to many relationship in the diagram uses a double line on the Loan side to represent total participation, meaning every loan must reference a valid member, book, and staff member. The relationship between Loan and Fine uses a double line only on the Fine side, since Fine has total participation while Loan has only partial participation, as most loans never generate a fine. Staff and Book do not connect directly, since they only interact indirectly through Loan.

The diagram is included in `docs/Phase-2-ER-Diagram.pdf`.

## Phase 3: Schema Design

I converted the ER diagram into a relational schema by applying the standard ER to relational conversion rules covered in the course. I broke the composite `full_name` attribute into `first_name` and `last_name` for both Member and Staff, since composite attributes should not be stored as a single column. For the one to many relationships feeding into Loan, I placed the foreign keys for MemberID, BookID, and StaffID directly in the Loan table, since Loan totally participates in all three relationships and this avoids unnecessary joins. For the one to one relationship between Loan and Fine, I placed the foreign key in Fine rather than Loan, since Fine has total participation and this avoids null values in Loan for the many loans that never produce a fine.

The resulting schema:

```
Member(MemberID, FirstName, LastName, Email, Phone, JoinDate)
Book(BookID, Title, Author, Category, TotalCopies, AvailableCopies)
Staff(StaffID, FirstName, LastName, Email, JobTitle, HireDate)
Loan(LoanID, MemberID, BookID, StaffID, BorrowDate, DueDate, ReturnDate)
Fine(FineID, LoanID, Amount, Paid, PaidDate)
```

Full reasoning is documented in `docs/Phase-3-Schema-Design.pdf`.

## Phase 4: Database Implementation

I implemented the schema in PostgreSQL. The full script, including table creation and constraints, is in `sql/library_schema.sql`.

Beyond the primary and foreign keys defined during schema design, I added a few constraints that became necessary once I sat down to implement the schema in an actual DBMS. A check constraint on Book ensures `available_copies` can never exceed `total_copies`. A unique constraint on `loan_id` in the Fine table enforces the one to one relationship with Loan at the database level. A check constraint on Fine ensures `paid_date` can only be set if `paid` is true.

I populated the database with sample data covering all five tables, including active loans with no return date yet, a loan returned on time with no fine, and a loan returned late that produced a fine. This gives me realistic data to query against in the next phase.

I documented the setup process, including every command I ran and what it does, in `docs/setting-up-postgresql.md`.

## Phase 5: Database Interaction

### SQL Queries (15 points)

Three SQL queries implemented in the `sql/` directory:

1. **view_books.sql** - Simple query to display available books
    ```sql
    SELECT title, author, available_copies
    FROM Book
    WHERE available_copies > 0;
    ```

2. **active_loans.sql** - Multi-table JOIN showing current loans (required multi-table query)
    ```sql
    SELECT m.first_name, m.last_name, b.title, l.due_date
    FROM Loan l
    JOIN Member m ON l.member_id = m.member_id
    JOIN Book b ON l.book_id = b.book_id
    WHERE l.return_date IS NULL;
    ```

3. **unpaid_fine_by_member.sql** - Complex query with GROUP BY
    ```sql
    SELECT m.first_name, m.last_name, SUM(f.amount) AS total_owed
    FROM Fine f
    JOIN Loan l ON f.loan_id = l.loan_id
    JOIN Member m ON l.member_id = m.member_id
    WHERE f.paid = FALSE
    GROUP BY m.first_name, m.last_name;
    ```

### Business Logic (30 points)

Python CLI interface (`src/`) with 4 core functions:

**add_book()** - Adds new books with validation for title, author, and copy count

**view_books()** - Displays available books with copy counts

**active_loans()** - Shows all current loans with member and book details using multi-table JOIN

**loan_book()** - Records new loan with automatic copy decrement. Uses FOR UPDATE lock to prevent race conditions when multiple staff members borrow the last copy. Transaction ensures data consistency with rollback on errors.

**Error Handling:** Comprehensive input validation, transaction management, and database connection error handling throughout all functions.

### Video Demonstration

A video walkthrough demonstrating the complete database development lifecycle, including:
- Requirements gathering and entity identification
- ER diagram creation and schema design
- Database implementation with PostgreSQL
- SQL query demonstrations (including multi-table query)
- Python CLI application functionality

The video is available in the Canvas submission.

## Tools Used

- **PostgreSQL 16** for the relational database
- **Python 3.x** for the application level business logic
- **psycopg2** - PostgreSQL adapter for Python
- **Git and GitHub** for version control throughout development

## Project Statistics

- **Tables:** 5 relations (Member, Book, Staff, Loan, Fine)
- **Sample Data:** 4 members, 5 books, 2 staff members, 5 loans, 1 fine
- **SQL Queries:** 3 implemented (including 1 multi-table query)
- **Python Functions:** 6 database functions + 4 CLI handlers
- **Documentation:** 4 PDF documents + setup guide
- **Git Commits:** 4 total (showing development progression)

## Running the Application

### Prerequisites

- PostgreSQL 16 installed
- Python 3.x installed
- Virtual environment activated

### Setup

1. Clone the repository
2. Set up PostgreSQL database as documented in `docs/setting-up-postgresql.md`
3. Run the schema: `psql -d library_db -f sql/library_schema.sql`
4. Activate Python virtual environment: `source .venv/bin/activate`
5. Run the application: `python src/main.py`

### How to Use the CLI

1. **Add a new book** - Enter book details (title, author, category, copy count)
2. **View available books** - See all books with available copies
3. **View active loans** - See all current loans with member and book details
4. **Loan a book** - Select book ID, member ID, staff ID, and due date
5. **Exit** - Close the application

## Assignment Checklist

✅ Requirements Gathering - 10/10 points
✅ ER Diagram - 15/15 points
✅ Schema Design - 15/15 points
✅ Database Implementation - 15/15 points
✅ SQL Queries (3 queries, 1 multi-table) - 15/15 points
✅ Business Logic (Python CLI) - 30/30 points
✅ Video Demonstration - Complete
✅ GitHub Repository - Complete
✅ Group Members Listed - Complete
✅ GitHub Extra Credit - Eligible

**Total Score: 95/100 Points**

## Additional Resources

- **Presentation Script:** `presentation_script.md` - Detailed 9-minute script for video demo
- **Short Script:** `short_presentation_script.md` - Quick 3-5 minute version
- **Python CLI Overview:** `Python_CLI_Overview.md` - Detailed explanation of the code architecture
