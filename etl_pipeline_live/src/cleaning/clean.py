import pandas as pd


# --------------------------------------------------
# Clean Food Delivery Orders
# --------------------------------------------------

def clean_orders(df):

    df = df.copy()

    # ----------------------------------------------
    # 1. Remove duplicate rows
    # ----------------------------------------------

    df = df.drop_duplicates(
        subset=["order_id"]
    )

    # ----------------------------------------------
    # 2. Convert numeric columns
    # ----------------------------------------------

    numeric_columns = [
        "order_id",
        "customer_id",
        "restaurant_id",
        "item_count",
        "order_amount",
        "discount",
        "delivery_fee",
        "rating",
        "delivery_time_minutes"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # ----------------------------------------------
    # 3. Convert timestamp
    # ----------------------------------------------

    df["order_timestamp"] = pd.to_datetime(
        df["order_timestamp"],
        errors="coerce"
    )

    # ----------------------------------------------
    # 4. Clean text columns
    # ----------------------------------------------

    text_columns = [
        "city",
        "restaurant_category",
        "order_status",
        "payment_method",
        "delivery_type"
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # ----------------------------------------------
    # 5. Standardize city names
    # ----------------------------------------------

    df["city"] = (
        df["city"]
        .str.title()
    )

    # ----------------------------------------------
    # 6. Standardize category names
    # ----------------------------------------------

    df["restaurant_category"] = (
        df["restaurant_category"]
        .str.title()
    )

    # ----------------------------------------------
    # 7. Remove impossible numeric values
    # ----------------------------------------------

    df = df[
        df["item_count"] > 0
    ]

    df = df[
        df["order_amount"] > 0
    ]

    df = df[
        df["discount"] >= 0
    ]

    df = df[
        df["delivery_fee"] >= 0
    ]

    # ----------------------------------------------
    # 8. Handle rating
    # ----------------------------------------------

    invalid_rating = (
        df["rating"].notna()
        & (
            (df["rating"] < 1)
            | (df["rating"] > 5)
        )
    )

    df.loc[
        invalid_rating,
        "rating"
    ] = pd.NA

    # ----------------------------------------------
    # 9. Handle delivery time
    # ----------------------------------------------

    invalid_delivery_time = (
        df["delivery_time_minutes"].notna()
        & (
            df["delivery_time_minutes"] <= 0
        )
    )

    df.loc[
        invalid_delivery_time,
        "delivery_time_minutes"
    ] = pd.NA

    # ----------------------------------------------
    # 10. Reset index
    # ----------------------------------------------

    df = df.reset_index(
        drop=True
    )

    return df


# --------------------------------------------------
# Test Cleaning
# --------------------------------------------------

if __name__ == "__main__":

    from pathlib import Path

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    processed_dir = (
        project_root
        / "data"
        / "processed"
    )

    input_file = (
        processed_dir
        / "valid_orders.csv"
    )

    output_file = (
        processed_dir
        / "clean_orders.csv"
    )

    if not input_file.exists():

        print(
            "valid_orders.csv not found."
        )

        print(
            "Run validation first."
        )

        raise SystemExit

    df = pd.read_csv(
        input_file
    )

    print()
    print("=" * 60)
    print("CLEANING DATA")
    print("=" * 60)

    print(
        f"Records before cleaning: {len(df)}"
    )

    cleaned_df = clean_orders(
        df
    )

    cleaned_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Records after cleaning : {len(cleaned_df)}"
    )

    print()
    print(
        f"Clean data saved to:"
    )

    print(output_file)

    print("=" * 60)