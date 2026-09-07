from pathlib import Path
import pandas as pd

from src.validation.validate import validate_orders
from src.cleaning.clean import clean_orders
from src.transformation.transform import transform_orders
from src.load.load_postgres import load_orders
from src.logging_config import logger


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

INCOMING_DIR = DATA_DIR / "incoming"
PROCESSED_DIR = DATA_DIR / "processed"
REJECTED_DIR = DATA_DIR / "rejected"
STATE_DIR = DATA_DIR / "state"

PROCESSED_FILES = STATE_DIR / "processed_files.txt"


# --------------------------------------------------
# Create required folders
# --------------------------------------------------

def create_directories():

    INCOMING_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    REJECTED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    STATE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not PROCESSED_FILES.exists():

        PROCESSED_FILES.touch()


# --------------------------------------------------
# Read processed file list
# --------------------------------------------------

def get_processed_files():

    if not PROCESSED_FILES.exists():
        return set()

    with open(
        PROCESSED_FILES,
        "r",
        encoding="utf-8"
    ) as file:

        return {
            line.strip()
            for line in file
            if line.strip()
        }


# --------------------------------------------------
# Mark file as processed
# --------------------------------------------------

def mark_file_as_processed(file_path):

    with open(
        PROCESSED_FILES,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            file_path.name + "\n"
        )


# --------------------------------------------------
# Find new/unprocessed file
# --------------------------------------------------

def get_new_file():

    files = list(
        INCOMING_DIR.glob("*.csv")
    )

    if not files:

        raise FileNotFoundError(
            "No CSV files found in data/incoming/"
        )

    processed_files = get_processed_files()

    new_files = [
        file
        for file in files
        if file.name not in processed_files
    ]

    if not new_files:

        return None

    # Process the oldest new file first
    new_file = min(
        new_files,
        key=lambda file: file.stat().st_mtime
    )

    return new_file


# --------------------------------------------------
# Run ETL Pipeline
# --------------------------------------------------

def run_pipeline():

    logger.info("=" * 70)
    logger.info("ETL PIPELINE STARTED")
    logger.info("=" * 70)

    print()
    print("=" * 70)
    print("STARTING ETL PIPELINE")
    print("=" * 70)

    # --------------------------------------------------
    # Prepare directories
    # --------------------------------------------------

    create_directories()

    logger.info("Required directories checked/created")

    # --------------------------------------------------
    # 1. EXTRACT
    # --------------------------------------------------

    print()
    print("STEP 1: EXTRACT")
    print("-" * 70)

    logger.info("STEP 1: EXTRACT")

    input_file = get_new_file()

    if input_file is None:

        print("No new files to process.")
        logger.info("No new files found in data/incoming/")
        logger.info("Pipeline finished - nothing to process.")

        return

    print(
        f"Reading file: {input_file.name}"
    )

    logger.info(
        f"Reading input file: {input_file.name}"
    )

    try:

        df = pd.read_csv(
            input_file
        )

    except Exception as error:

        logger.exception(
            f"Failed to read file: {input_file.name}"
        )

        print(
            f"ERROR reading file: {error}"
        )

        return

    print(
        f"Records extracted: {len(df)}"
    )

    logger.info(
        f"Records extracted: {len(df)}"
    )

    # --------------------------------------------------
    # 2. VALIDATE
    # --------------------------------------------------

    print()
    print("STEP 2: VALIDATE")
    print("-" * 70)

    logger.info("STEP 2: VALIDATE")

    try:

        valid_df, rejected_df = validate_orders(
            df
        )

    except Exception as error:

        logger.exception(
            f"Validation failed for {input_file.name}"
        )

        print(
            f"ERROR during validation: {error}"
        )

        return

    print(
        f"Valid records: {len(valid_df)}"
    )

    print(
        f"Rejected records: {len(rejected_df)}"
    )

    logger.info(
        f"Valid records: {len(valid_df)}"
    )

    logger.info(
        f"Rejected records: {len(rejected_df)}"
    )

    # --------------------------------------------------
    # Save rejected records
    # --------------------------------------------------

    if not rejected_df.empty:

        rejected_file = (
            REJECTED_DIR
            / f"{input_file.stem}_rejected.csv"
        )

        rejected_df.to_csv(
            rejected_file,
            index=False
        )

        print(
            f"Rejected data saved to: "
            f"{rejected_file}"
        )

        logger.warning(
            f"Rejected data saved to: "
            f"{rejected_file}"
        )

    # --------------------------------------------------
    # Stop if nothing is valid
    # --------------------------------------------------

    if valid_df.empty:

        print()
        print("No valid records available.")
        print("Pipeline stopped.")

        logger.warning(
            f"No valid records in {input_file.name}"
        )

        # Mark the file as processed because
        # validation has been completed.
        mark_file_as_processed(
            input_file
        )

        return

    # --------------------------------------------------
    # 3. CLEAN
    # --------------------------------------------------

    print()
    print("STEP 3: CLEAN")
    print("-" * 70)

    logger.info("STEP 3: CLEAN")

    try:

        clean_df = clean_orders(
            valid_df
        )

    except Exception as error:

        logger.exception(
            f"Cleaning failed for {input_file.name}"
        )

        print(
            f"ERROR during cleaning: {error}"
        )

        return

    clean_file = (
        PROCESSED_DIR
        / f"{input_file.stem}_clean.csv"
    )

    clean_df.to_csv(
        clean_file,
        index=False
    )

    print(
        f"Records after cleaning: "
        f"{len(clean_df)}"
    )

    print(
        f"Clean data saved to: "
        f"{clean_file}"
    )

    logger.info(
        f"Records after cleaning: {len(clean_df)}"
    )

    logger.info(
        f"Clean data saved to: {clean_file}"
    )

    # --------------------------------------------------
    # 4. TRANSFORM
    # --------------------------------------------------

    print()
    print("STEP 4: TRANSFORM")
    print("-" * 70)

    logger.info("STEP 4: TRANSFORM")

    try:

        transformed_df = transform_orders(
            clean_df
        )

    except Exception as error:

        logger.exception(
            f"Transformation failed for {input_file.name}"
        )

        print(
            f"ERROR during transformation: {error}"
        )

        return

    transformed_file = (
        PROCESSED_DIR
        / f"{input_file.stem}_transformed.csv"
    )

    transformed_df.to_csv(
        transformed_file,
        index=False
    )

    print(
        f"Records after transformation: "
        f"{len(transformed_df)}"
    )

    print(
        f"Transformed data saved to: "
        f"{transformed_file}"
    )

    logger.info(
        f"Records after transformation: "
        f"{len(transformed_df)}"
    )

    logger.info(
        f"Transformed data saved to: "
        f"{transformed_file}"
    )

    # --------------------------------------------------
    # 5. LOAD
    # --------------------------------------------------

    print()
    print("STEP 5: LOAD")
    print("-" * 70)

    logger.info("STEP 5: LOAD")

    try:

        inserted = load_orders(
            transformed_df
        )

    except Exception as error:

        logger.exception(
            "PostgreSQL loading failed"
        )

        print(
            f"ERROR loading data into PostgreSQL: "
            f"{error}"
        )

        return

    print(
        f"Records inserted into PostgreSQL: "
        f"{inserted}"
    )

    logger.info(
        f"Records inserted into PostgreSQL: "
        f"{inserted}"
    )

    # --------------------------------------------------
    # Mark input file as processed
    # --------------------------------------------------

    mark_file_as_processed(
        input_file
    )

    logger.info(
        f"File marked as processed: "
        f"{input_file.name}"
    )

    # --------------------------------------------------
    # PIPELINE COMPLETE
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print()
    print(
        f"Input records:       {len(df)}"
    )

    print(
        f"Valid records:       {len(valid_df)}"
    )

    print(
        f"Rejected records:    {len(rejected_df)}"
    )

    print(
        f"Transformed records: {len(transformed_df)}"
    )

    print(
        f"Database inserted:   {inserted}"
    )

    print(
        f"Processed file:      {input_file.name}"
    )

    print()

    logger.info(
        f"Input records: {len(df)}"
    )

    logger.info(
        f"Valid records: {len(valid_df)}"
    )

    logger.info(
        f"Rejected records: {len(rejected_df)}"
    )

    logger.info(
        f"Transformed records: {len(transformed_df)}"
    )

    logger.info(
        f"Database inserted: {inserted}"
    )

    logger.info(
        "ETL PIPELINE COMPLETED SUCCESSFULLY"
    )

    logger.info("=" * 70)


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    run_pipeline()