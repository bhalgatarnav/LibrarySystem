# Library Management System - Video Presentation Script

**Total Duration:** 5-8 minutes
**Tone:** Professional, clear, and conversational
**Target:** Instructor for CS4092 Database Design and Development

---

## [0:00-0:45] Introduction (45 seconds)

**(Visual: Show GitHub repository link and project README opening)**

"Hello! My name is Arnav Bhalgat, and today I'll be presenting my final project for the Database Design and Development course (CS4092).

This is a **Library Management System** - a complete backend database system that I designed following the entire database development lifecycle. I've adapted this from the course's sample e-commerce project, applying all the concepts I've learned to build a functional relational database for a library."

---

## [0:45-1:30] Project Overview (45 seconds)

**(Visual: Show the project structure directory)**

"The system supports two user roles:

1. **Staff members** who can add and edit books in the catalog, view all books, view a member's loan history, record returns, and generate fines

2. **Members** who can browse the catalog, borrow books, and view their own loan and fine history

I chose this domain because it naturally requires many of the concepts we've learned - constraints, relationships, transactions, and querying across multiple tables."

---

## [1:30-3:00] Phase 1: Requirements Gathering (1.5 minutes)

**(Visual: Open `docs/Phase-1-Requirements.pdf`)**

"**Phase 1: Requirements Gathering**

I started by identifying all the use cases for both Staff and Members. For Staff, I documented:
- Adding books to the catalog
- Editing book information
- Viewing all books
- Recording book returns
- Generating and managing fines

For Members:
- Registering for an account
- Browsing available books
- Borrowing books
- Viewing loan history and fines

From these use cases, I identified **five core entities**: Member, Book, Staff, Loan, and Fine.

I also documented key assumptions that shaped the design:
- A member can only borrow **one copy of a given book at a time** - we track total copies vs. available copies rather than individual physical copies
- A loan is considered **active until a return date** is recorded
- **Fines are only generated when a book is returned late** - payment processing is outside the scope of this project

This requirements document (147 KB) serves as the foundation for everything else in the project."

---

## [3:00-4:30] Phase 2 & 3: ER Diagram and Schema Design (1.5 minutes)

**(Visual: Open `docs/Phase-2-ER-Diagram.pdf` then `Phase-3-Schema-Design.pdf`)**

"**Phase 2: Entity-Relationship Diagram**

I created an ER diagram showing the relationships between these five entities. The diagram uses standard notation with double lines representing total participation - meaning every Loan must reference a valid Member, Book, and Staff member.

**Phase 3: Schema Design**

I converted the ER diagram into a relational schema using standard ER-to-relational conversion rules.

Key design decisions:
1. I **decomposed composite attributes** like `full_name` into `first_name` and `last_name` for both Member and Staff tables - composite attributes shouldn't be stored as a single column
2. For the one-to-many relationships, I placed foreign keys directly in the Loan table to avoid unnecessary joins
3. For the one-to-one relationship between Loan and Fine, I placed the foreign key in Fine rather than Loan - this avoids NULL values in Loan for the many loans that never produce a fine

The final schema is:
```
Member(member_id, first_name, last_name, email, phone, join_date)
Book(book_id, title, author, category, total_copies, available_copies)
Staff(staff_id, first_name, last_name, email, job_title, hire_date)
Loan(loan_id, member_id, book_id, staff_id, borrow_date, due_date, return_date)
Fine(fine_id, loan_id, amount, paid, paid_date)
```

These design choices ensure data integrity and optimize query performance."

---

## [4:30-5:30] Phase 4: Database Implementation (1 minute)

**(Visual: Open `sql/library_schema.sql` and show key sections)**

"**Phase 4: Database Implementation**

I implemented this schema in **PostgreSQL**, using the file `library_schema.sql` (123 lines).

I added several constraints beyond the basic schema:
- A CHECK constraint on Book ensures `available_copies` can never exceed `total_copies`
- A UNIQUE constraint on `loan_id` in the Fine table enforces the one-to-one relationship at the database level
- A CHECK constraint on Fine ensures `paid_date` can only be set if `paid` is TRUE

I populated all five tables with **sample data**:
- **4 Members**: Ava Thompson, Liam Chen, Sofia Martinez, Noah Patel
- **5 Books**: Database System Concepts, Clean Code, The Great Gatsby, A Brief History of Time, Introduction to Algorithms
- **2 Staff Members**: Grace Kim and Marcus Johnson
- **5 Loans**: including 2 active loans, 2 completed loans, and 1 late return that generated a fine
- **1 Fine**: $4.50 for the late return

This realistic data set gives me scenarios to query and demonstrate the system."

---

## [5:30-6:45] Phase 5: SQL Queries (1.15 minutes)

**(Visual: Open PostgreSQL and run the three SQL queries)**

"**Phase 5: Database Interaction - SQL Queries**

Here are the three SQL queries I implemented:

**Query 1: View Available Books**
```sql
SELECT title, author, available_copies
FROM Book
WHERE available_copies > 0;
```
This simple query shows all books that have copies available for borrowing.

**Query 2: View Active Loans - Multi-table Query**
```sql
SELECT m.first_name, m.last_name, b.title, l.due_date
FROM Loan l
JOIN Member m ON l.member_id = m.member_id
JOIN Book b ON l.book_id = b.book_id
WHERE l.return_date IS NULL;
```
This query joins three tables to show which members currently have active loans, including the due dates. This is the **multi-table query** required by the assignment.

**Query 3: Unpaid Fines by Member**
```sql
SELECT m.first_name, m.last_name, SUM(f.amount) AS total_owed
FROM Fine f
JOIN Loan l ON f.loan_id = l.loan_id
JOIN Member m ON l.member_id = m.member_id
WHERE f.paid = FALSE
GROUP BY m.first_name, m.last_name;
```
This joins three tables and uses GROUP BY to calculate how much each member owes in unpaid fines."

---

## [6:45-8:15] Business Logic - Python CLI (1.5 minutes)

**(Visual: Show the Python CLI application running with screenshots or screen recording)**

"**Business Logic: Python CLI Interface**

I implemented a command-line interface using Python and the psycopg2 PostgreSQL adapter. The code is in the `src/` directory with three main files:

`db.py` - Database connection management
`queries.py` - SQL query functions
`main.py` - CLI interface with user menu

**Features implemented:**

1. **Add a new book** - Staff can input title, author, category, and copy count. The system validates input and inserts into the database.

2. **View available books** - Displays all books with available copies, formatted with titles, authors, and copy counts.

3. **View active loans** - Shows all current loans with member names, book titles, and due dates.

4. **Loan a book** - The most complex feature. When a staff member loans a book:
   - The system first displays available books with their IDs
   - User selects a book ID, member ID, staff ID, and due date
   - The system validates all IDs are positive integers
   - It uses a FOR UPDATE lock to prevent race conditions if two staff members try to borrow the last copy at the same time
   - It inserts a new loan record AND decrements the available copy count in the same transaction
   - If any error occurs, it rolls back the transaction

**Code quality highlights:**
- Proper input validation before database access
- Transaction management with rollback on errors
- Comprehensive error handling for database connections
- Formatted output with visual indicators (✓ for success, ✗ for errors)
- Clean, commented code that follows Python best practices"

---

## [8:15-9:00] Conclusion and Technical Highlights (45 seconds)

**(Visual: Show final summary of what was accomplished)**

"To summarize what I've built:

- **A complete relational database** with 5 properly normalized tables
- **Comprehensive documentation** spanning all 5 phases of the database development lifecycle
- **Production-quality SQL code** with 3 queries including a multi-table JOIN
- **A functional Python CLI** with proper transaction management, error handling, and input validation
- **Realistic test data** covering all edge cases

I used Git and GitHub throughout development, making frequent commits as I progressed through each phase - this has been documented in the git log and will be available for the extra credit opportunity.

This project has given me hands-on experience with the entire database development lifecycle, from requirements gathering to implementation to application-level interaction - exactly what this course is designed to teach."

---

## [9:00-9:30] Q&A and Thank You (30 seconds)

"Thank you for watching! I'm happy to answer any questions about the database design, the SQL queries, the Python code, or the development process.

The complete source code and documentation are available in my GitHub repository at [INSERT YOUR GITHUB URL HERE].

This concludes my presentation."

---

## Tips for Recording:

1. **Screen recording** your screen while demonstrating each phase
2. **Show the actual code** running (PostgreSQL queries, Python CLI)
3. **Pause briefly** when showing PDF documents to give time to read
4. **Speak clearly** and at a moderate pace
5. **Highlight key concepts** as you demonstrate them
6. **Show error cases** briefly (if you have time) to demonstrate error handling
7. **Keep it conversational** - you're explaining to a human, not reading from a script
8. **Practice 2-3 times** before recording for the final version