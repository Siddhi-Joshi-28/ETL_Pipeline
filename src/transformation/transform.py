import pandas as pd
from pathlib import Path

from src.extract.extract import extract_data
from src.validation.validate import validate_data
from src.cleaning.clean import clean_data


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

    print("=" * 50)
    print("TRANSFORMATION STAGE")
    print("=" * 50)

    df = df.copy()

    # -------------------------------------------------
    # 1. Make sure created_at is datetime
    # -------------------------------------------------

    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce"
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

    # -------------------------------------------------
    # 3. Add pipeline processing timestamp
    # -------------------------------------------------

    df["processed_at"] = pd.Timestamp.now()

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

    # -------------------------------------------------
    # Print results
    # -------------------------------------------------

    print(f"Input records       : {len(df)}")
    print(f"Output records      : {len(df)}")
    print(f"Output columns      : {len(df.columns)}")
    print(f"Processed file      : {PROCESSED_FILE}")

    print("\nFinal columns:")
    print(list(df.columns))

    print("=" * 50)

    return df


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