import pandas as pd

from src.extract.extract import extract_data
from src.validation.validate import validate_data
from src.logging_config import get_logger


logger = get_logger(__name__)


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

    logger.info("Cleaning stage started")

    print("=" * 50)
    print("CLEANING STAGE")
    print("=" * 50)

    try:
        # Work on a copy
        df = df.copy()

        original_count = len(df)

        logger.info(
            f"Cleaning input records: {original_count}"
        )

        # -------------------------------------------------
        # 1. Remove duplicate question IDs
        # -------------------------------------------------

        df = df.drop_duplicates(
            subset=["question_id"],
            keep="first"
        )

        duplicates_removed = original_count - len(df)

        logger.info(
            f"Duplicate records removed: {duplicates_removed}"
        )

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

        before_missing_removal = len(df)

        df = df.dropna(
            subset=required_columns
        )

        missing_values_removed = (
            before_missing_removal - len(df)
        )

        logger.info(
            f"Records removed due to missing values: "
            f"{missing_values_removed}"
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

        logger.info("Category values standardized")

        # -------------------------------------------------
        # 4. Clean city
        # -------------------------------------------------

        df["city"] = (
            df["city"]
            .astype(str)
            .str.strip()
            .str.title()
        )

        logger.info("City values standardized")

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

        logger.info("Question text cleaned")

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

        logger.info(
            "Numeric columns converted successfully"
        )

        # -------------------------------------------------
        # 7. Convert timestamp
        # -------------------------------------------------

        df["created_at"] = pd.to_datetime(
            df["created_at"],
            errors="coerce"
        )

        # Remove records where timestamp conversion failed
        before_timestamp_removal = len(df)

        df = df.dropna(
            subset=["created_at"]
        )

        invalid_timestamp_removed = (
            before_timestamp_removal - len(df)
        )

        if invalid_timestamp_removed > 0:
            logger.warning(
                f"Records removed due to invalid timestamps: "
                f"{invalid_timestamp_removed}"
            )
        else:
            logger.info(
                "All timestamps converted successfully"
            )

        # -------------------------------------------------
        # Final results
        # -------------------------------------------------

        total_removed = original_count - len(df)

        logger.info(
            f"Cleaning completed | "
            f"Original: {original_count} | "
            f"Clean: {len(df)} | "
            f"Removed: {total_removed}"
        )

        print(f"Original records     : {original_count}")
        print(f"Duplicates removed   : {duplicates_removed}")
        print(f"Clean records        : {len(df)}")
        print(f"Records removed      : {total_removed}")

        print("\nData types after cleaning:")
        print(df.dtypes)

        print("=" * 50)

        return df

    except Exception as error:

        logger.error(
            f"Cleaning stage failed: {error}"
        )

        raise


if __name__ == "__main__":

    # Step 1: Extract
    raw_df = extract_data()

    # Step 2: Validate
    valid_df, invalid_df = validate_data(raw_df)

    # Step 3: Clean
    clean_df = clean_data(valid_df)

    print("\nFirst 5 cleaned records:")
    print(clean_df.head())