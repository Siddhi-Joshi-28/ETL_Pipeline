-- =====================================================
-- HelloQ ETL Pipeline - Analytics Queries
-- =====================================================

-- -----------------------------------------------------
-- 1. Total number of questions
-- -----------------------------------------------------

SELECT COUNT(*) AS total_questions
FROM questions;


-- -----------------------------------------------------
-- 2. Total number of users
-- -----------------------------------------------------

SELECT COUNT(*) AS total_users
FROM users;


-- -----------------------------------------------------
-- 3. Questions by category
-- -----------------------------------------------------

SELECT
    category,
    COUNT(*) AS total_questions
FROM questions
GROUP BY category
ORDER BY total_questions DESC;


-- -----------------------------------------------------
-- 4. Questions by city
-- -----------------------------------------------------

SELECT
    city,
    COUNT(*) AS total_questions
FROM questions
GROUP BY city
ORDER BY total_questions DESC;


-- -----------------------------------------------------
-- 5. Questions by year
-- -----------------------------------------------------

SELECT
    created_year,
    COUNT(*) AS total_questions
FROM questions
GROUP BY created_year
ORDER BY created_year;


-- -----------------------------------------------------
-- 6. Questions by month
-- -----------------------------------------------------

SELECT
    created_month,
    COUNT(*) AS total_questions
FROM questions
GROUP BY created_month
ORDER BY created_month;


-- -----------------------------------------------------
-- 7. Questions asked by each user
-- -----------------------------------------------------

SELECT
    user_id,
    COUNT(*) AS total_questions
FROM questions
GROUP BY user_id
ORDER BY total_questions DESC;


-- -----------------------------------------------------
-- 8. Top 10 users by number of questions
-- -----------------------------------------------------

SELECT
    user_id,
    COUNT(*) AS total_questions
FROM questions
GROUP BY user_id
ORDER BY total_questions DESC
LIMIT 10;


-- -----------------------------------------------------
-- 9. Latest 10 questions
-- -----------------------------------------------------

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


-- -----------------------------------------------------
-- 10. Questions by category and city
-- -----------------------------------------------------

SELECT
    category,
    city,
    COUNT(*) AS total_questions
FROM questions
GROUP BY category, city
ORDER BY total_questions DESC;