-- Remove all entries with duplicate emails
DELETE FROM users
WHERE email IN (
    SELECT * FROM (SELECT email
    FROM users
    GROUP BY email
    HAVING COUNT(*) > 1)tableTmp);


ALTER TABLE users
ADD CONSTRAINT unique_email UNIQUE (email);
