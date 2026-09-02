import pandas as pd
from pathlib import Path

from src.extract.extract import extract_data


# Find project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Rejected records location
REJECTED_DIR = PROJECT_ROOT / "data" / "rejected"
REJECTED_FILE = REJECTED_DIR / "invalid_questions.csv"


# Required columns
REQUIRED_COLUMNS = [
    "question_id",
    "user_id",
    "category",
    "city",
    "question_text",
    "created_at",
]


def validate_data(df):
    """
    Validate raw HelloQ question data.

    Returns:
        valid_df: Records that pass validation.
        invalid_df: Records that fail validation.
    """

    print("=" * 50)
    print("VALIDATION STAGE")
    print("=" * 50)

    # Make a copy so the original DataFrame is not changed
    df = df.copy()

    invalid_mask = pd.Series(False, index=df.index)

    # -------------------------------------------------
    # 1. Check required columns
    # -------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # -------------------------------------------------
    # 2. Check missing required values
    # -------------------------------------------------

    required_value_missing = (
        df[REQUIRED_COLUMNS]
        .isnull()
        .any(axis=1)
    )

    invalid_mask |= required_value_missing

    # -------------------------------------------------
    # 3. Check question_id
    # -------------------------------------------------

    invalid_question_id = (
        pd.to_numeric(
            df["question_id"],
            errors="coerce"
        ).isnull()
    )

    invalid_mask |= invalid_question_id

    # -------------------------------------------------
    # 4. Check user_id
    # -------------------------------------------------

    invalid_user_id = (
        pd.to_numeric(
            df["user_id"],
            errors="coerce"
        ).isnull()
    )

    invalid_mask |= invalid_user_id

    # -------------------------------------------------
    # 5. Check timestamp
    # -------------------------------------------------

    invalid_timestamp = (
        pd.to_datetime(
            df["created_at"],
            errors="coerce"
        ).isnull()
    )

    invalid_mask |= invalid_timestamp

    # -------------------------------------------------
    # Separate valid and invalid records
    # -------------------------------------------------

    invalid_df = df[invalid_mask].copy()
    valid_df = df[~invalid_mask].copy()

    # -------------------------------------------------
    # Save rejected records
    # -------------------------------------------------

    if not invalid_df.empty:

        REJECTED_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        invalid_df.to_csv(
            REJECTED_FILE,
            index=False
        )

    # -------------------------------------------------
    # Print validation results
    # -------------------------------------------------

    print(f"Total records   : {len(df)}")
    print(f"Valid records   : {len(valid_df)}")
    print(f"Invalid records : {len(invalid_df)}")

    if not invalid_df.empty:
        print(f"Rejected file   : {REJECTED_FILE}")
    else:
        print("No invalid records found.")

    print("=" * 50)

    return valid_df, invalid_df


if __name__ == "__main__":

    # Extract raw data
    df = extract_data()

    # Validate data
    valid_df, invalid_df = validate_data(df)