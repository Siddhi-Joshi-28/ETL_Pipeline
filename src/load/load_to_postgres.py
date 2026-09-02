import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv


# -------------------------------------------------
# Project paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "helloq_questions_processed.csv"
)


# -------------------------------------------------
# Load environment variables
# -------------------------------------------------

load_dotenv(PROJECT_ROOT / ".env")


# -------------------------------------------------
# PostgreSQL connection
# -------------------------------------------------

def get_connection():
    """
    Create a connection to PostgreSQL.
    """

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


# -------------------------------------------------
# Load data
# -------------------------------------------------

def load_data():

    print("=" * 50)
    print("LOAD STAGE")
    print("=" * 50)

    # Check processed file
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"Processed file not found: {PROCESSED_FILE}"
        )

    # Read transformed data
    df = pd.read_csv(PROCESSED_FILE)

    print(f"Records to load: {len(df)}")

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # -----------------------------------------
        # Insert users
        # -----------------------------------------

        user_ids = df["user_id"].dropna().unique()

        for user_id in user_ids:

            cursor.execute(
                """
                INSERT INTO users (user_id)
                VALUES (%s)
                ON CONFLICT (user_id) DO NOTHING;
                """,
                (int(user_id),)
            )

        print(f"Users processed: {len(user_ids)}")

        # -----------------------------------------
        # Insert questions
        # -----------------------------------------

        for _, row in df.iterrows():

            cursor.execute(
                """
                INSERT INTO questions (
                    question_id,
                    user_id,
                    category,
                    city,
                    question_text,
                    created_at,
                    created_date,
                    created_month,
                    created_year,
                    processed_at
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                ON CONFLICT (question_id) DO UPDATE SET
                    user_id = EXCLUDED.user_id,
                    category = EXCLUDED.category,
                    city = EXCLUDED.city,
                    question_text = EXCLUDED.question_text,
                    created_at = EXCLUDED.created_at,
                    created_date = EXCLUDED.created_date,
                    created_month = EXCLUDED.created_month,
                    created_year = EXCLUDED.created_year,
                    processed_at = EXCLUDED.processed_at;
                """,
                (
                    int(row["question_id"]),
                    int(row["user_id"]),
                    row["category"],
                    row["city"],
                    row["question_text"],
                    row["created_at"],
                    row["created_date"],
                    row["created_month"],
                    int(row["created_year"]),
                    row["processed_at"],
                )
            )

        # Save changes
        connection.commit()

        print(f"Questions loaded: {len(df)}")
        print("Database loading completed successfully.")

    except Exception as error:

        connection.rollback()

        print("Database loading failed.")
        print(f"Error: {error}")

        raise

    finally:

        cursor.close()
        connection.close()

    print("=" * 50)


if __name__ == "__main__":
    load_data()