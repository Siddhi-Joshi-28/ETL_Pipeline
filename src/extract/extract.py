import pandas as pd
from pathlib import Path


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

    if not RAW_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {RAW_DATA_FILE}"
        )

    df = pd.read_csv(RAW_DATA_FILE)

    print("=" * 50)
    print("EXTRACT STAGE")
    print("=" * 50)
    print(f"Source file : {RAW_DATA_FILE}")
    print(f"Rows        : {len(df)}")
    print(f"Columns     : {len(df.columns)}")
    print("=" * 50)

    return df


if __name__ == "__main__":
    df = extract_data()

    print("\nFirst 5 records:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)