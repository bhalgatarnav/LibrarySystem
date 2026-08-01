-- view the available books to loan
SELECT title, author, available_copies
FROM Book
WHERE available_copies > 0;