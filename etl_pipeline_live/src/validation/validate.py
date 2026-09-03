import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Allowed Values
# --------------------------------------------------

VALID_ORDER_STATUSES = {
    "Delivered",
    "Cancelled",
    "Pending"
}


VALID_PAYMENT_METHODS = {
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Wallet"
}


VALID_DELIVERY_TYPES = {
    "Normal",
    "Express"
}


# --------------------------------------------------
# Required Columns
# --------------------------------------------------

REQUIRED_COLUMNS = [
    "order_id",
    "customer_id",
    "restaurant_id",
    "order_timestamp",
    "city",
    "restaurant_category",
    "order_status",
    "payment_method",
    "delivery_type",
    "item_count",
    "order_amount",
    "discount",
    "delivery_fee",
    "rating",
    "delivery_time_minutes"
]


# --------------------------------------------------
# Validate Data
# --------------------------------------------------

def validate_orders(df):

    valid_mask = pd.Series(
        True,
        index=df.index
    )

    errors = pd.Series(
        "",
        index=df.index
    )

    # ----------------------------------------------
    # Required columns
    # ----------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # ----------------------------------------------
    # Required values
    # ----------------------------------------------

    required_fields = [
        "order_id",
        "customer_id",
        "restaurant_id",
        "city",
        "restaurant_category",
        "order_status",
        "payment_method",
        "delivery_type"
    ]

    for column in required_fields:

        mask = df[column].isna()

        valid_mask &= ~mask

        errors.loc[mask] += (
            f"{column} is missing; "
        )

    # ----------------------------------------------
    # Duplicate order IDs
    # ----------------------------------------------

    duplicate_mask = (
        df["order_id"].duplicated(
            keep=False
        )
    )

    valid_mask &= ~duplicate_mask

    errors.loc[duplicate_mask] += (
        "Duplicate order_id; "
    )

    # ----------------------------------------------
    # Order status
    # ----------------------------------------------

    invalid_status = ~df[
        "order_status"
    ].isin(
        VALID_ORDER_STATUSES
    )

    valid_mask &= ~invalid_status

    errors.loc[invalid_status] += (
        "Invalid order_status; "
    )

    # ----------------------------------------------
    # Payment method
    # ----------------------------------------------

    invalid_payment = ~df[
        "payment_method"
    ].isin(
        VALID_PAYMENT_METHODS
    )

    valid_mask &= ~invalid_payment

    errors.loc[invalid_payment] += (
        "Invalid payment_method; "
    )

    # ----------------------------------------------
    # Delivery type
    # ----------------------------------------------

    invalid_delivery = ~df[
        "delivery_type"
    ].isin(
        VALID_DELIVERY_TYPES
    )

    valid_mask &= ~invalid_delivery

    errors.loc[invalid_delivery] += (
        "Invalid delivery_type; "
    )

    # ----------------------------------------------
    # Item count
    # ----------------------------------------------

    invalid_items = (
        pd.to_numeric(
            df["item_count"],
            errors="coerce"
        ) <= 0
    )

    valid_mask &= ~invalid_items

    errors.loc[invalid_items] += (
        "item_count must be greater than 0; "
    )

    # ----------------------------------------------
    # Order amount
    # ----------------------------------------------

    invalid_amount = (
        pd.to_numeric(
            df["order_amount"],
            errors="coerce"
        ) <= 0
    )

    valid_mask &= ~invalid_amount

    errors.loc[invalid_amount] += (
        "order_amount must be greater than 0; "
    )

    # ----------------------------------------------
    # Discount
    # ----------------------------------------------

    invalid_discount = (
        pd.to_numeric(
            df["discount"],
            errors="coerce"
        ) < 0
    )

    valid_mask &= ~invalid_discount

    errors.loc[invalid_discount] += (
        "discount cannot be negative; "
    )

    # ----------------------------------------------
    # Delivery fee
    # ----------------------------------------------

    invalid_fee = (
        pd.to_numeric(
            df["delivery_fee"],
            errors="coerce"
        ) < 0
    )

    valid_mask &= ~invalid_fee

    errors.loc[invalid_fee] += (
        "delivery_fee cannot be negative; "
    )

    # ----------------------------------------------
    # Rating
    # ----------------------------------------------

    rating_numeric = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    invalid_rating = (
        df["rating"].notna()
        & (
            (rating_numeric < 1)
            | (rating_numeric > 5)
        )
    )

    valid_mask &= ~invalid_rating

    errors.loc[invalid_rating] += (
        "rating must be between 1 and 5; "
    )

    # ----------------------------------------------
    # Delivery time
    # ----------------------------------------------

    delivery_time_numeric = pd.to_numeric(
        df["delivery_time_minutes"],
        errors="coerce"
    )

    invalid_delivery_time = (
        df["delivery_time_minutes"].notna()
        & (
            delivery_time_numeric <= 0
        )
    )

    valid_mask &= ~invalid_delivery_time

    errors.loc[invalid_delivery_time] += (
        "delivery_time must be positive; "
    )

    # ----------------------------------------------
    # Create results
    # ----------------------------------------------

    valid_df = df[
        valid_mask
    ].copy()

    rejected_df = df[
        ~valid_mask
    ].copy()

    rejected_df["validation_error"] = (
        errors[
            ~valid_mask
        ]
    )

    return valid_df, rejected_df


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    incoming_dir = (
        project_root
        / "data"
        / "incoming"
    )

    processed_dir = (
        project_root
        / "data"
        / "processed"
    )

    rejected_dir = (
        project_root
        / "data"
        / "rejected"
    )

    # Create directories if they don't exist

    processed_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    rejected_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Find incoming files

    files = sorted(
        incoming_dir.glob(
            "orders_*.csv"
        )
    )

    if not files:

        print(
            "No incoming order files found."
        )

        raise SystemExit

    # Process the latest incoming file

    latest_file = files[-1]

    print(
        f"Reading: {latest_file.name}"
    )

    df = pd.read_csv(
        latest_file
    )

    # Validate

    valid_df, rejected_df = (
        validate_orders(df)
    )

    # Save valid records

    valid_file = (
        processed_dir
        / "valid_orders.csv"
    )

    valid_df.to_csv(
        valid_file,
        index=False
    )

    # Save rejected records

    rejected_file = (
        rejected_dir
        / "invalid_orders.csv"
    )

    if not rejected_df.empty:

        rejected_df.to_csv(
            rejected_file,
            index=False
        )

    print()
    print("=" * 60)
    print("VALIDATION RESULT")
    print("=" * 60)

    print(
        f"Total records    : {len(df)}"
    )

    print(
        f"Valid records    : {len(valid_df)}"
    )

    print(
        f"Rejected records : {len(rejected_df)}"
    )

    print()
    print(
        f"Valid data saved to:"
    )

    print(valid_file)

    print()

    if not rejected_df.empty:

        print(
            "Rejected data saved to:"
        )

        print(rejected_file)

    else:

        print(
            "No rejected records."
        )

    print("=" * 60)