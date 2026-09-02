# HelloQ ETL Pipeline

This project demonstrates an ETL pipeline using synthetic HelloQ question data.

The dataset contains around 1,000 questions and 30 users.

The pipeline extracts, validates, cleans, transforms, and loads the data into PostgreSQL. SQL is then used for analysis, and a Streamlit dashboard displays the results.

---

## ETL Architecture

Raw CSV
  ↓
Extract
  ↓
Validate
  ↓
Clean
  ↓
Transform
  ↓
Processed CSV
  ↓
PostgreSQL
  ↓
SQL Analytics
  ↓
Streamlit Dashboard

---

## Technologies Used

- Python
- Pandas
- PostgreSQL
- psycopg2
- SQL
- pytest
- python-dotenv
- Streamlit
- Git
- GitHub

---

## Project Features

### 1. Extract

Reads raw HelloQ question data from CSV using Pandas.

### 2. Validate

Checks:

- Required columns
- Missing values
- question_id
- user_id
- created_at

Invalid records are saved in:

```text
data/rejected/invalid_questions.csv
```

### 3. Clean

- Removes duplicate question IDs
- Removes missing required values
- Standardizes categories
- Standardizes cities
- Cleans question text
- Converts IDs to numeric types
- Converts timestamps

### 4. Transform

Creates:

- created_date
- created_month
- created_year
- processed_at

Output:

```text
data/processed/helloq_questions_processed.csv
```

### 5. Load

Loads processed data into PostgreSQL.

Database:

```text
helloq_db
```

Tables:

```text
users
questions
```

Duplicate question IDs are handled using `ON CONFLICT`.

### 6. Logging

Logs important pipeline events and errors.

Log file:

```text
logs/etl_pipeline.log
```

### 7. Testing

The project uses pytest to test:

- Extraction
- Validation
- Cleaning
- Transformation

Run:

```bash
pytest -v
```

### 8. Dashboard

`app.py` contains the Streamlit dashboard.

The dashboard displays:

- Total Questions
- Total Users
- Categories
- Cities
- Questions by Category
- Questions by City
- Questions Over Time
- Top Users
- Latest Questions

Run:

```bash
streamlit run app.py
```

---

## Project Structure

```text
HelloQ_ETL_Pipeline/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
│
├── sql/
│   └── analytics.sql
│
├── src/
│   ├── extract/
│   │   └── extract.py
│   ├── validation/
│   │   └── validate.py
│   ├── cleaning/
│   │   └── clean.py
│   ├── transformation/
│   │   └── transform.py
│   ├── load/
│   │   └── load_to_postgres.py
│   ├── logging_config.py
│   └── pipeline.py
│
├── tests/
│   ├── conftest.py
│   ├── test_extract.py
│   ├── test_validation.py
│   ├── test_cleaning.py
│   └── test_transformation.py
│
├── logs/
├── app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Database

PostgreSQL database:

```text
helloq_db
```

Tables:

```text
users
questions
```

---

## Analytics

SQL analytics include:

- Total questions
- Total users
- Questions by category
- Questions by city
- Questions by year
- Questions by month
- Questions per user
- Top users
- Latest questions

SQL file:

```text
sql/analytics.sql
```

---

## How to Run

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure PostgreSQL

Create:

```text
helloq_db
```

Create `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=helloq_db
DB_USER=postgres
DB_PASSWORD=your_password
```

Do not upload `.env` to GitHub.

### Step 3: Run ETL Pipeline

```bash
python -m src.pipeline
```

### Step 4: Run Tests

```bash
pytest -v
```

### Step 5: Run Analytics

Open:

```text
sql/analytics.sql
```

and run the required queries in PostgreSQL.

### Step 6: Run Dashboard

```bash
streamlit run app.py
```

Open the Streamlit URL shown in the terminal.

---

## Complete Flow

```text
1. Raw CSV
2. Extract
3. Validate
4. Clean
5. Transform
6. Save Processed CSV
7. Load into PostgreSQL
8. Run SQL Analytics
9. Run Tests
10. Start Streamlit Dashboard
```

---

## Dataset

The demo dataset contains:

- Approximately 1,000 questions
- 30 users

The data is synthetic and is used for testing and demonstrating the ETL pipeline.

---

## Learning Objectives

This project demonstrates:

- ETL Pipeline
- Data Validation
- Data Cleaning
- Data Transformation
- PostgreSQL
- SQL
- Python Logging
- Error Handling
- Automated Testing
- Streamlit Dashboard
- Git and GitHub
