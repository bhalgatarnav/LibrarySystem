-- using join for this result
SELECT m.first_name, m.last_name, b.title, l.due_date
FROM Loan l
JOIN Member m ON l.member_id = m.member_id
JOIN Book b ON l.book_id = b.book_id
WHERE l.return_date IS NULL;