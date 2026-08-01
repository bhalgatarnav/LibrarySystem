# Short Presentation Script (3-5 minutes)

**For quick demo or if time is limited**

---

## [0:00-0:30] Introduction (30 seconds)

"Hi, I'm Arnav Bhalgat and I've built a Library Management System for my CS4092 Database Design and Development final project. This is a complete backend database that follows the full database development lifecycle."

---

## [0:30-1:15] Requirements & Design (45 seconds)

"I started with requirements gathering, identifying 5 core entities: Member, Book, Staff, Loan, and Fine. I created an ER diagram showing the relationships, then converted it to a relational schema with proper primary keys, foreign keys, and constraints."

---

## [1:15-2:00] Implementation (45 seconds)

"I implemented this in PostgreSQL with 5 tables. Key features include checking that available copies never exceed total copies, enforcing the one-to-one Loan-Fine relationship, and populating realistic test data with members, books, staff, loans, and fines."

---

## [2:00-3:30] SQL Queries (1.5 minutes)

"I implemented three SQL queries. The first is a simple query to view available books. The second is a multi-table query joining Loan, Member, and Book to show active loans. The third uses joins and GROUP BY to calculate unpaid fines per member. This meets the requirement for at least one multi-table query."

---

## [3:30-5:00] Python CLI (1.5 minutes)

"Instead of just writing queries, I built a Python CLI application. It has four main features: add a new book, view available books, view active loans, and loan a book. The loan function is the most complex - it uses transaction management with FOR UPDATE locks to prevent race conditions when multiple staff members borrow the last copy. The code includes input validation, error handling, and proper database rollback on failures."

---

## [5:00-5:30] Conclusion (30 seconds)

"This project demonstrates the complete database development lifecycle - from requirements to implementation to application interaction. The code is clean, well-documented, and ready for use. Thanks for watching!"

---

## Quick Recording Checklist:

✓ Show GitHub repository
✓ Demonstrate 3 SQL queries running
✓ Show Python CLI application working
✓ Highlight key features (transaction management, error handling)
✓ Mention you used Git throughout development