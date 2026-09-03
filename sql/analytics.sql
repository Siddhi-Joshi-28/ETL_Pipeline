-- ============================================
-- HelloQ ETL Pipeline - SQL Analytics
-- ============================================

-- 1. Total Questions
SELECT COUNT(*) AS total_questions
FROM questions;


-- 2. Total Users
SELECT COUNT(*) AS total_users
FROM users;


-- 3. Questions by Category
SELECT
    category,
    COUNT(*) AS question_count
FROM questions
GROUP BY category
ORDER BY question_count DESC;


-- 4. Questions by City
SELECT
    city,
    COUNT(*) AS question_count
FROM questions
GROUP BY city
ORDER BY question_count DESC;


-- 5. Questions by Year
SELECT
    created_year,
    COUNT(*) AS question_count
FROM questions
GROUP BY created_year
ORDER BY created_year;


-- 6. Questions by Month
SELECT
    created_month,
    COUNT(*) AS question_count
FROM questions
GROUP BY created_month
ORDER BY created_month;


-- 7. Questions per User
SELECT
    user_id,
    COUNT(*) AS question_count
FROM questions
GROUP BY user_id
ORDER BY question_count DESC;


-- 8. Top 10 Users
SELECT
    user_id,
    COUNT(*) AS question_count
FROM questions
GROUP BY user_id
ORDER BY question_count DESC
LIMIT 10;


-- 9. Latest Questions
SELECT
    question_id,
    user_id,
    category,
    city,
    question_text,
    created_at
FROM questions
ORDER BY created_at DESC
LIMIT 10;


-- 10. Category + City Analysis
SELECT
    category,
    city,
    COUNT(*) AS question_count
FROM questions
GROUP BY category, city
ORDER BY question_count DESC;