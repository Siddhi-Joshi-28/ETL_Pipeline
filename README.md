# HelloQ ETL Pipeline

A Python-based ETL pipeline designed to process HelloQ question data.

The pipeline extracts raw question data from CSV, validates and cleans
the data, transforms it into an analytics-ready format, and loads the
final data into PostgreSQL.

---

## ETL Architecture

Raw CSV Data
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
Analytics SQL


---

## Technologies Used

- Python
- Pandas
- PostgreSQL
- psycopg2
- SQL
- pytest
- python-dotenv
- Git
- GitHub


---

## Project Features

### 1. Data Extraction

Reads raw HelloQ question data from a CSV file.

### 2. Data Validation

Checks:

- Required columns
- Missing required values
- question_id
- user_id
- created_at timestamp

Invalid records are stored separately.

### 3. Data Cleaning

The cleaning stage:

- Removes duplicate question IDs
- Removes records with missing required values
- Standardizes categories
- Standardizes cities
- Cleans question text
- Converts numeric IDs
- Converts timestamps

### 4. Data Transformation

The transformation stage creates:

- created_date
- created_month
- created_year
- processed_at

The transformed data is saved as:

data/processed/helloq_questions_processed.csv

### 5. PostgreSQL Loading

The transformed data is loaded into PostgreSQL.

The database contains:

- users
- questions

Duplicate question IDs are handled using PostgreSQL
ON CONFLICT logic.

### 6. Logging

The pipeline records important events such as:

- Pipeline started
- Records extracted
- Validation results
- Cleaning results
- Transformation results
- Database connection
- Records loaded
- Pipeline completion
- Errors

Logs are stored in:

logs/etl_pipeline.log

### 7. Testing

The project uses pytest to test:

- Extraction
- Validation
- Cleaning
- Transformation

Run all tests with:

pytest -v


---

## Project Structure

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
│   │
│   ├── validation/
│   │   └── validate.py
│   │
│   ├── cleaning/
│   │   └── clean.py
│   │
│   ├── transformation/
│   │   └── transform.py
│   │
│   ├── load/
│   │   └── load_to_postgres.py
│   │
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
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md


---

## Database

PostgreSQL is used as the final data storage system.

Database:

helloq_db

Tables:

users
questions


---

## Example Analytics

The project includes SQL queries for:

- Total questions
- Total users
- Questions by category
- Questions by city
- Questions by year
- Questions by month
- Questions per user
- Top users
- Latest questions
- Category and city analysis

The queries are available in:

sql/analytics.sql


---

## How to Run

### 1. Clone the repository

git clone <your-github-repository-url>

cd HelloQ_ETL_Pipeline


### 2. Install dependencies

pip install -r requirements.txt


### 3. Configure PostgreSQL

Create a PostgreSQL database named:

helloq_db

Configure the database credentials in `.env`.

Example:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=helloq_db
DB_USER=postgres
DB_PASSWORD=your_password


Do not upload `.env` to GitHub.


### 4. Run the complete ETL pipeline

python -m src.pipeline


### 5. Run tests

pytest -v


---

## Data Flow

The pipeline processes data in the following order:

Raw CSV
  ↓
Extraction
  ↓
Validation
  ↓
Rejected Records
  ↓
Cleaning
  ↓
Transformation
  ↓
Processed CSV
  ↓
PostgreSQL
  ↓
Analytics


---

## Current Dataset

The demonstration dataset contains approximately:

- 1,000 questions
- 30 users

The pipeline is designed so that the same process can be used
with larger datasets.

---

## Learning Objectives

This project demonstrates practical understanding of:

- ETL pipeline design
- Data validation
- Data cleaning
- Data transformation
- PostgreSQL
- SQL analytics
- Python logging
- Error handling
- Automated testing
- Git and GitHub