
SELECT
    category,
    COUNT(*) AS question_count
FROM questions
GROUP BY category
ORDER BY question_count DESC;


SELECT
    city,
    COUNT(*) AS question_count
FROM questions
GROUP BY city
ORDER BY question_count DESC;

SELECT COUNT(*)
FROM questions;

SELECT category, COUNT(*)
FROM questions
GROUP BY category;

SELECT
    category,
    COUNT(*) AS question_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM questions),
        2
    ) AS percentage
FROM questions
GROUP BY category
ORDER BY question_count DESC;