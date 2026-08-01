-- here we combine joins with groupby
SELECT m.first_name, m.last_name, SUM(f.amount) AS total_owed
FROM Fine f
JOIN Loan l ON f.loan_id = l.loan_id
JOIN Member m ON l.member_id = m.member_id
WHERE f.paid = FALSE
GROUP BY m.first_name, m.last_name;