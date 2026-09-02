import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv

from src.logging_config import get_logger


logger = get_logger(__name__)


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

    logger.info("Connecting to PostgreSQL")

    try:

        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

        logger.info("PostgreSQL connection successful")

        return connection

    except Exception as error:

        logger.error(
            f"PostgreSQL connection failed: {error}"
        )

        raise


# -------------------------------------------------
# Load data
# -------------------------------------------------

def load_data():

    logger.info("Load stage started")

    print("=" * 50)
    print("LOAD STAGE")
    print("=" * 50)

    # -------------------------------------------------
    # Check processed file
    # -------------------------------------------------

    if not PROCESSED_FILE.exists():

        logger.error(
            f"Processed file not found: {PROCESSED_FILE}"
        )

        raise FileNotFoundError(
            f"Processed file not found: {PROCESSED_FILE}"
        )

    logger.info(
        f"Processed file found: {PROCESSED_FILE}"
    )

    # -------------------------------------------------
    # Read transformed data
    # -------------------------------------------------

    try:

        df = pd.read_csv(PROCESSED_FILE)

        logger.info(
            f"Processed data loaded | Records: {len(df)}"
        )

    except Exception as error:

        logger.error(
            f"Failed to read processed data: {error}"
        )

        raise

    print(f"Records to load: {len(df)}")

    connection = None
    cursor = None

    try:

        # -------------------------------------------------
        # Connect to PostgreSQL
        # -------------------------------------------------

        connection = get_connection()

        cursor = connection.cursor()

        # -----------------------------------------
        # Insert users
        # -----------------------------------------

        user_ids = df["user_id"].dropna().unique()

        logger.info(
            f"Processing {len(user_ids)} unique users"
        )

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

        logger.info(
            f"Users processed successfully: {len(user_ids)}"
        )

        # -----------------------------------------
        # Insert questions
        # -----------------------------------------

        logger.info(
            f"Starting question loading: {len(df)} records"
        )

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
                    row["created_year"],
                    row["processed_at"],
                )
            )

        # -------------------------------------------------
        # Save changes
        # -------------------------------------------------

        connection.commit()

        print(f"Questions loaded: {len(df)}")
        print("Database loading completed successfully.")

        logger.info(
            f"Questions loaded successfully: {len(df)}"
        )

        logger.info(
            "PostgreSQL transaction committed successfully"
        )

        logger.info(
            "Load stage completed"
        )

    except Exception as error:

        if connection:
            connection.rollback()

        print("Database loading failed.")
        print(f"Error: {error}")

        logger.error(
            f"Database loading failed: {error}"
        )

        logger.info(
            "PostgreSQL transaction rolled back"
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

        logger.info(
            "PostgreSQL connection closed"
        )

    print("=" * 50)


if __name__ == "__main__":
    load_data()