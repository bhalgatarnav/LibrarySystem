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
│   ├── Phase-1-Requirements.pdf
│   ├── Phase-2-ER-Diagram.pdf
│   ├── Phase-3-Schema-Design.pdf
│   └── setting-up-postgresql.md
├── sql/
│   └── library_schema.sql
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

Not yet started. This phase will include at least three SQL queries, with at least one multi table query, along with a Python command line interface for adding and viewing books, and a video walkthrough demonstrating both.

## Tools Used

- **PostgreSQL 16** for the relational database
- **Python** for the application level business logic, added in Phase 5
- **Git and GitHub** for version control throughout development
