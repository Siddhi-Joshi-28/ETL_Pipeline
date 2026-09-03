import requests
import pandas as pd
from pathlib import Path


API_URL = (
    "http://127.0.0.1:5000/api/orders"
)


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]


INCOMING_DIR = (
    PROJECT_ROOT
    / "data"
    / "incoming"
)


def extract_orders():

    response = requests.get(
        API_URL,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    orders = data.get(
        "orders",
        []
    )

    df = pd.DataFrame(
        orders
    )

    return df


def save_incoming_data(df):

    INCOMING_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = pd.Timestamp.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = (
        INCOMING_DIR
        / f"orders_{timestamp}.csv"
    )

    df.to_csv(
        file_path,
        index=False
    )

    return file_path


if __name__ == "__main__":

    df = extract_orders()

    print()
    print("=" * 70)
    print("API EXTRACTION")
    print("=" * 70)

    print(
        f"Records received: {len(df)}"
    )

    file_path = save_incoming_data(
        df
    )

    print(
        f"Saved to: {file_path}"
    )

    print()
    print(df.to_string(
        index=False
    ))

    print("=" * 70)