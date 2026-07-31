-- ============================================================
-- Library Management System
-- Database Design and Development (CS4092) - Final Project
-- Phase 4: Database Implementation
-- DBMS: PostgreSQL
-- ============================================================

-- handle the errors where the tabe would exist first
DROP TABLE IF EXISTS Fine;
DROP TABLE IF EXISTS Loan;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Member;

-- ============================================================
-- Using DDL Commands
-- ============================================================
CREATE TABLE Member (
    member_id     SERIAL PRIMARY KEY,
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    phone         VARCHAR(20),
    join_date     DATE         NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE Book (
    book_id           SERIAL PRIMARY KEY,
    title             VARCHAR(200) NOT NULL,
    author            VARCHAR(100) NOT NULL,
    category          VARCHAR(50),
    total_copies      INT NOT NULL CHECK (total_copies >= 0),
    available_copies  INT NOT NULL CHECK (available_copies >= 0),
    CHECK (available_copies <= total_copies)
);

CREATE TABLE Staff (
    staff_id      SERIAL PRIMARY KEY,
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    job_title     VARCHAR(50),
    hire_date     DATE NOT NULL
);

CREATE TABLE Loan (
    loan_id       SERIAL PRIMARY KEY,
    -- REFERENCES Member(member_id) guarantees anyone cannot assign a member_id 
    -- to a loan if that member does not exist in the Member table.
    member_id     INT NOT NULL REFERENCES Member(member_id) ON DELETE RESTRICT,
    -- we also need ON DELETE RESTRICT as a record cannot be deleted from the parent
    -- table if its ref exists in Loan
    book_id       INT NOT NULL REFERENCES Book(book_id) ON DELETE RESTRICT,
    staff_id      INT NOT NULL REFERENCES Staff(staff_id) ON DELETE RESTRICT,
    borrow_date   DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date      DATE NOT NULL,
    return_date   DATE,
    
    CHECK (due_date >= borrow_date),
    CHECK (return_date IS NULL OR return_date >= borrow_date)
);

CREATE TABLE Fine (
    fine_id       SERIAL PRIMARY KEY,
    -- UNIQUE will enforce a 1-to-1 relationship: one loan can only ever produce one fine.
    -- REFERENCES Loan(loan_id) means a fine cannot exist unless its loan_id exists in Loan.
    loan_id       INT NOT NULL UNIQUE REFERENCES Loan(loan_id),
    amount        DECIMAL(6,2) NOT NULL CHECK (amount >= 0),
    -- BOOLEAN holds either TRUE or FALSE. DEFAULT FALSE will ensure we assume nothing is paid
    paid          BOOLEAN NOT NULL DEFAULT FALSE,
    paid_date     DATE,
    
    CHECK (paid_date IS NULL OR paid = TRUE)
);

-- ============================================================
-- SAMPLE DATA
-- ============================================================

-- Members
INSERT INTO Member (first_name, last_name, email, phone, join_date) VALUES
('Ava', 'Thompson', 'ava.thompson@email.com', '513-555-0101', '2025-01-10'),
('Liam', 'Chen', 'liam.chen@email.com', '513-555-0102', '2025-02-14'),
('Sofia', 'Martinez', 'sofia.martinez@email.com', '513-555-0103', '2025-03-05'),
('Noah', 'Patel', 'noah.patel@email.com', '513-555-0104', '2025-04-22');

-- Books
INSERT INTO Book (title, author, category, total_copies, available_copies) VALUES
('Database System Concepts', 'Silberschatz', 'Technology', 3, 2),
('Clean Code', 'Robert Martin', 'Technology', 2, 2),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 4, 3),
('A Brief History of Time', 'Stephen Hawking', 'Science', 2, 1),
('Introduction to Algorithms', 'Cormen', 'Technology', 3, 3);

-- Staff
INSERT INTO Staff (first_name, last_name, email, job_title, hire_date) VALUES
('Grace', 'Kim', 'grace.kim@library.org', 'Librarian', '2022-06-01'),
('Marcus', 'Johnson', 'marcus.johnson@library.org', 'Assistant Librarian', '2023-09-15');

-- Loans
-- Loan 1: returned on time, no fine
INSERT INTO Loan (member_id, book_id, staff_id, borrow_date, due_date, return_date) VALUES
(1, 1, 1, '2026-06-01', '2026-06-15', '2026-06-10');

-- Loan 2: returned late, will have a fine
INSERT INTO Loan (member_id, book_id, staff_id, borrow_date, due_date, return_date) VALUES
(2, 4, 2, '2026-06-05', '2026-06-19', '2026-06-25');

-- Loan 3: still active, not yet returned
INSERT INTO Loan (member_id, book_id, staff_id, borrow_date, due_date, return_date) VALUES
(3, 3, 1, '2026-07-20', '2026-08-03', NULL);

-- Loan 4: returned on time, no fine
INSERT INTO Loan (member_id, book_id, staff_id, borrow_date, due_date, return_date) VALUES
(1, 3, 2, '2026-05-01', '2026-05-15', '2026-05-14');

-- Loan 5: still active, not yet returned
INSERT INTO Loan (member_id, book_id, staff_id, borrow_date, due_date, return_date) VALUES
(4, 1, 1, '2026-07-25', '2026-08-08', NULL);

-- Fine tied to the late return in Loan 2
INSERT INTO Fine (loan_id, amount, paid, paid_date) VALUES
(2, 4.50, TRUE, '2026-06-26');
