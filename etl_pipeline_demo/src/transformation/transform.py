import pandas as pd
from pathlib import Path

from src.extract.extract import extract_data
from src.validation.validate import validate_data
from src.cleaning.clean import clean_data
from src.logging_config import get_logger


logger = get_logger(__name__)


# Find project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Processed data directory
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Output file
PROCESSED_FILE = PROCESSED_DIR / "helloq_questions_processed.csv"


def transform_data(df):
    """
    Transform cleaned HelloQ question data.

    Transformations:
    1. Standardize timestamp
    2. Create date/month/year columns
    3. Create processed_at timestamp
    4. Arrange columns for database loading
    """

    logger.info("Transformation stage started")

    print("=" * 50)
    print("TRANSFORMATION STAGE")
    print("=" * 50)

    try:

        df = df.copy()

        input_count = len(df)

        logger.info(
            f"Transformation input records: {input_count}"
        )

        # -------------------------------------------------
        # 1. Make sure created_at is datetime
        # -------------------------------------------------

        df["created_at"] = pd.to_datetime(
            df["created_at"],
            errors="coerce"
        )

        logger.info(
            "created_at converted to datetime"
        )

        # -------------------------------------------------
        # 2. Create date information
        # -------------------------------------------------

        df["created_date"] = df["created_at"].dt.date

        df["created_month"] = (
            df["created_at"]
            .dt.to_period("M")
            .astype(str)
        )

        df["created_year"] = (
            df["created_at"]
            .dt.year
        )

        logger.info(
            "Created date, month and year columns"
        )

        # -------------------------------------------------
        # 3. Add pipeline processing timestamp
        # -------------------------------------------------

        df["processed_at"] = pd.Timestamp.now()

        logger.info(
            "Added processed_at timestamp"
        )

        # -------------------------------------------------
        # 4. Arrange columns
        # -------------------------------------------------

        columns = [
            "question_id",
            "user_id",
            "category",
            "city",
            "question_text",
            "created_at",
            "created_date",
            "created_month",
            "created_year",
            "processed_at",
        ]

        df = df[columns]

        logger.info(
            f"Columns arranged | Total columns: {len(df.columns)}"
        )

        # -------------------------------------------------
        # 5. Save transformed data
        # -------------------------------------------------

        PROCESSED_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_csv(
            PROCESSED_FILE,
            index=False
        )

        logger.info(
            f"Transformed data saved to: {PROCESSED_FILE}"
        )

        # -------------------------------------------------
        # Print results
        # -------------------------------------------------

        print(f"Input records       : {input_count}")
        print(f"Output records      : {len(df)}")
        print(f"Output columns      : {len(df.columns)}")
        print(f"Processed file      : {PROCESSED_FILE}")

        print("\nFinal columns:")
        print(list(df.columns))

        print("=" * 50)

        logger.info(
            f"Transformation completed | "
            f"Input: {input_count} | "
            f"Output: {len(df)} | "
            f"Columns: {len(df.columns)}"
        )

        return df

    except Exception as error:

        logger.error(
            f"Transformation stage failed: {error}"
        )

        raise


if __name__ == "__main__":

    # 1. Extract
    raw_df = extract_data()

    # 2. Validate
    valid_df, invalid_df = validate_data(raw_df)

    # 3. Clean
    clean_df = clean_data(valid_df)

    # 4. Transform
    transformed_df = transform_data(clean_df)

    print("\nFirst 5 transformed records:")
    print(transformed_df.head())