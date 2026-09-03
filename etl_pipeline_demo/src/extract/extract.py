import pandas as pd
from pathlib import Path

from src.logging_config import get_logger


logger = get_logger(__name__)


# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Location of raw HelloQ data
RAW_DATA_FILE = PROJECT_ROOT / "data" / "raw" / "helloq_questions_raw.csv"


def extract_data():
    """
    Extract raw HelloQ question data from CSV.

    Returns:
        pandas.DataFrame: Raw HelloQ question data.
    """

    logger.info("Extract stage started")

    # Check whether raw data file exists
    if not RAW_DATA_FILE.exists():
        logger.error(
            f"Raw data file not found: {RAW_DATA_FILE}"
        )

        raise FileNotFoundError(
            f"Raw data file not found: {RAW_DATA_FILE}"
        )

    try:
        # Read raw CSV file
        df = pd.read_csv(RAW_DATA_FILE)

        logger.info(
            f"Extracted {len(df)} records"
        )

        logger.info(
            f"Extracted {len(df.columns)} columns"
        )

        logger.info("Extract stage completed")

        print("=" * 50)
        print("EXTRACT STAGE")
        print("=" * 50)
        print(f"Source file : {RAW_DATA_FILE}")
        print(f"Rows        : {len(df)}")
        print(f"Columns     : {len(df.columns)}")
        print("=" * 50)

        return df

    except Exception as error:

        logger.error(
            f"Extract stage failed: {error}"
        )

        raise


if __name__ == "__main__":
    df = extract_data()

    print("\nFirst 5 records:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)