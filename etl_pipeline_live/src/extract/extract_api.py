import requests
import pandas as pd
from pathlib import Path

from src.logging_config import get_logger

logger = get_logger()


# ============================================================
# API CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:5000/api/orders"


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


INCOMING_DIR = (
    PROJECT_ROOT
    / "data"
    / "incoming"
)


# ============================================================
# EXTRACT DATA FROM API
# ============================================================

def extract_orders():

    response = requests.get(
        API_URL,
        timeout=10
    )

    # Stop if API gives an error
    response.raise_for_status()

    # Convert API response to Python dictionary
    data = response.json()

    # Get orders from API response
    orders = data.get(
        "orders",
        []
    )

    # Convert orders into DataFrame
    df = pd.DataFrame(
        orders
    )

    return df


# ============================================================
# SAVE RAW / INCOMING DATA
# ============================================================

def save_incoming_data(df):

    # Create incoming folder if it doesn't exist
    INCOMING_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Create timestamp
    timestamp = pd.Timestamp.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    # Create file name
    file_path = (
        INCOMING_DIR
        / f"orders_{timestamp}.csv"
    )

    # Save EXACT data received from API
    df.to_csv(
        file_path,
        index=False
    )

    return file_path


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # STEP 1: EXTRACT
    # --------------------------------------------------------

    logger.info("Starting API extraction")

    df = extract_orders()

    logger.info(
        f"API extraction completed. Records received: {len(df)}"
    )


    # --------------------------------------------------------
    # SHOW EXTRACTION INFORMATION
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("API EXTRACTION")
    print("=" * 70)

    print(
        f"Records received: {len(df)}"
    )


    # --------------------------------------------------------
    # SHOW BATCH SIZE
    # --------------------------------------------------------

    if len(df) == 10:
 
        print(
            "Batch size: EXACTLY 10 records"
        )

    elif len(df) < 10:

        print(
            f"Batch size: {len(df)} records "
            "(less than 10)"
        )

    else:

        print(
            f"Batch size: {len(df)} records "
            "(more than 10)"
        )


    # --------------------------------------------------------
    # SAVE RAW DATA
    # --------------------------------------------------------

    file_path = save_incoming_data(
       df
    )

    logger.info(
        f"Incoming file saved: {file_path}"
    )

    # --------------------------------------------------------
    # SHOW DATA
    # --------------------------------------------------------

    print()
    print("RAW DATA RECEIVED FROM API")
    print("-" * 70)

    print(
        df.to_string(
            index=False
        )
    )


    print("=" * 70)