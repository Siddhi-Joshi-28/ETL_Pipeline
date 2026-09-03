CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    question_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    created_date DATE,
    created_month VARCHAR(7),
    created_year INTEGER,
    processed_at TIMESTAMP,

    CONSTRAINT fk_questions_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE INDEX IF NOT EXISTS idx_questions_user_id
ON questions(user_id);

CREATE INDEX IF NOT EXISTS idx_questions_category
ON questions(category);

CREATE INDEX IF NOT EXISTS idx_questions_city
ON questions(city);

CREATE INDEX IF NOT EXISTS idx_questions_created_at
ON questions(created_at);

