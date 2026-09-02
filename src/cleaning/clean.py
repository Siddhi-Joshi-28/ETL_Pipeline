import pandas as pd

from src.extract.extract import extract_data
from src.validation.validate import validate_data


def clean_data(df):
    """
    Clean validated HelloQ question data.

    Cleaning operations:
    1. Remove duplicate records
    2. Remove records with missing required values
    3. Standardize category
    4. Standardize city
    5. Clean question text
    6. Convert data types
    """

    print("=" * 50)
    print("CLEANING STAGE")
    print("=" * 50)

    # Work on a copy
    df = df.copy()

    original_count = len(df)

    # -------------------------------------------------
    # 1. Remove duplicate question IDs
    # -------------------------------------------------

    df = df.drop_duplicates(
        subset=["question_id"],
        keep="first"
    )

    duplicates_removed = original_count - len(df)

    # -------------------------------------------------
    # 2. Remove rows with missing required values
    # -------------------------------------------------

    required_columns = [
        "question_id",
        "user_id",
        "category",
        "city",
        "question_text",
        "created_at",
    ]

    df = df.dropna(
        subset=required_columns
    )

    # -------------------------------------------------
    # 3. Clean category
    # -------------------------------------------------

    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # -------------------------------------------------
    # 4. Clean city
    # -------------------------------------------------

    df["city"] = (
        df["city"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # -------------------------------------------------
    # 5. Clean question text
    # -------------------------------------------------

    df["question_text"] = (
        df["question_text"]
        .astype(str)
        .str.strip()
    )

    # Remove extra spaces inside text
    df["question_text"] = (
        df["question_text"]
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
    )

    # -------------------------------------------------
    # 6. Convert numeric columns
    # -------------------------------------------------

    df["question_id"] = pd.to_numeric(
        df["question_id"],
        errors="coerce"
    ).astype("Int64")

    df["user_id"] = pd.to_numeric(
        df["user_id"],
        errors="coerce"
    ).astype("Int64")

    # -------------------------------------------------
    # 7. Convert timestamp
    # -------------------------------------------------

    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce"
    )

    # Remove records where timestamp conversion failed
    df = df.dropna(
        subset=["created_at"]
    )

    # -------------------------------------------------
    # Final results
    # -------------------------------------------------

    print(f"Original records     : {original_count}")
    print(f"Duplicates removed   : {duplicates_removed}")
    print(f"Clean records        : {len(df)}")
    print(f"Records removed      : {original_count - len(df)}")

    print("\nData types after cleaning:")
    print(df.dtypes)

    print("=" * 50)

    return df


if __name__ == "__main__":

    # Step 1: Extract
    raw_df = extract_data()

    # Step 2: Validate
    valid_df, invalid_df = validate_data(raw_df)

    # Step 3: Clean
    clean_df = clean_data(valid_df)

    print("\nFirst 5 cleaned records:")
    print(clean_df.head())