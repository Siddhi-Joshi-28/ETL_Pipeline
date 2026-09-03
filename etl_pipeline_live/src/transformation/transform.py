import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Transform Food Delivery Orders
# --------------------------------------------------

def transform_orders(df):

    df = df.copy()

    # ----------------------------------------------
    # Convert timestamp
    # ----------------------------------------------

    df["order_timestamp"] = pd.to_datetime(
        df["order_timestamp"],
        errors="coerce"
    )

    # ----------------------------------------------
    # Calculate net amount
    # ----------------------------------------------

    df["net_amount"] = (
        df["order_amount"]
        - df["discount"]
        + df["delivery_fee"]
    )

    # ----------------------------------------------
    # Calculate discount percentage
    # ----------------------------------------------

    df["discount_percentage"] = (
        df["discount"]
        / df["order_amount"]
        * 100
    )

    # ----------------------------------------------
    # Date information
    # ----------------------------------------------

    df["order_date"] = (
        df["order_timestamp"]
        .dt.date
    )

    df["order_year"] = (
        df["order_timestamp"]
        .dt.year
    )

    df["order_month"] = (
        df["order_timestamp"]
        .dt.month
    )

    df["order_month_name"] = (
        df["order_timestamp"]
        .dt.month_name()
    )

    # ----------------------------------------------
    # Time information
    # ----------------------------------------------

    df["order_hour"] = (
        df["order_timestamp"]
        .dt.hour
    )

    # ----------------------------------------------
    # Day information
    # ----------------------------------------------

    df["order_day"] = (
        df["order_timestamp"]
        .dt.day_name()
    )

    # ----------------------------------------------
    # Delivery status flags
    # ----------------------------------------------

    df["is_delivered"] = (
        df["order_status"]
        == "Delivered"
    ).astype(int)

    df["is_cancelled"] = (
        df["order_status"]
        == "Cancelled"
    ).astype(int)

    df["is_pending"] = (
        df["order_status"]
        == "Pending"
    ).astype(int)

    # ----------------------------------------------
    # Delivery performance
    # ----------------------------------------------

    df["delivery_performance"] = "Unknown"

    delivered_mask = (
        df["delivery_time_minutes"]
        .notna()
    )

    df.loc[
        delivered_mask
        & (
            df["delivery_time_minutes"] <= 30
        ),
        "delivery_performance"
    ] = "Fast"

    df.loc[
        delivered_mask
        & (
            df["delivery_time_minutes"] > 30
        )
        & (
            df["delivery_time_minutes"] <= 60
        ),
        "delivery_performance"
    ] = "Normal"

    df.loc[
        delivered_mask
        & (
            df["delivery_time_minutes"] > 60
        ),
        "delivery_performance"
    ] = "Slow"

    # ----------------------------------------------
    # Average item price
    # ----------------------------------------------

    df["average_item_price"] = (
        df["order_amount"]
        / df["item_count"]
    )

    # ----------------------------------------------
    # Reset index
    # ----------------------------------------------

    df = df.reset_index(
        drop=True
    )

    return df


# --------------------------------------------------
# Run Transformation
# --------------------------------------------------

if __name__ == "__main__":

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
        / "clean_orders.csv"
    )

    output_file = (
        processed_dir
        / "transformed_orders.csv"
    )

    if not input_file.exists():

        print(
            "clean_orders.csv not found."
        )

        print(
            "Run cleaning first."
        )

        raise SystemExit

    df = pd.read_csv(
        input_file
    )

    print()
    print("=" * 60)
    print("TRANSFORMING DATA")
    print("=" * 60)

    print(
        f"Records received: {len(df)}"
    )

    transformed_df = transform_orders(
        df
    )

    transformed_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Records after transformation: "
        f"{len(transformed_df)}"
    )

    print()
    print("New analytics columns:")

    new_columns = [
        "net_amount",
        "discount_percentage",
        "order_date",
        "order_year",
        "order_month",
        "order_month_name",
        "order_hour",
        "order_day",
        "is_delivered",
        "is_cancelled",
        "is_pending",
        "delivery_performance",
        "average_item_price"
    ]

    print(
        new_columns
    )

    print()
    print(
        f"Transformed data saved to:"
    )

    print(output_file)

    print("=" * 60)