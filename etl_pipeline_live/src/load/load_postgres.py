import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)

load_dotenv(
    PROJECT_ROOT / ".env"
)


# --------------------------------------------------
# Database connection
# --------------------------------------------------

def get_connection():

    return psycopg2.connect(
        host=os.getenv(
            "POSTGRES_HOST",
            "localhost"
        ),
        port=os.getenv(
            "POSTGRES_PORT",
            "5432"
        ),
        database=os.getenv(
            "POSTGRES_DB",
            "food_delivery"
        ),
        user=os.getenv(
            "POSTGRES_USER",
            "postgres"
        ),
        password=os.getenv(
            "POSTGRES_PASSWORD"
        )
    )


# --------------------------------------------------
# Load transformed orders
# --------------------------------------------------

def load_orders(df):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        INSERT INTO orders (
            order_id,
            customer_id,
            restaurant_id,
            order_timestamp,
            city,
            restaurant_category,
            order_status,
            payment_method,
            delivery_type,
            item_count,
            order_amount,
            discount,
            delivery_fee,
            rating,
            delivery_time_minutes,
            net_amount,
            discount_percentage,
            order_date,
            order_year,
            order_month,
            order_month_name,
            order_hour,
            order_day,
            is_delivered,
            is_cancelled,
            is_pending,
            delivery_performance,
            average_item_price
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s
        )
        ON CONFLICT (order_id)
        DO NOTHING;
    """

    columns = [
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
        "delivery_time_minutes",
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

    inserted = 0

    for _, row in df.iterrows():

        values = [
            row[column]
            for column in columns
        ]

        # Convert pandas NaN to None
        values = [
            None if pd.isna(value)
            else value
            for value in values
        ]

        cursor.execute(
            query,
            values
        )

        if cursor.rowcount == 1:
            inserted += 1

    connection.commit()

    cursor.close()
    connection.close()

    return inserted


# --------------------------------------------------
# Run loader
# --------------------------------------------------

if __name__ == "__main__":

    input_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "transformed_orders.csv"
    )

    if not input_file.exists():

        print(
            "transformed_orders.csv not found."
        )

        print(
            "Run transformation first."
        )

        raise SystemExit

    df = pd.read_csv(
        input_file
    )

    print()
    print("=" * 60)
    print("LOADING DATA INTO POSTGRESQL")
    print("=" * 60)

    print(
        f"Records received: {len(df)}"
    )

    inserted = load_orders(
        df
    )

    print(
        f"Records inserted: {inserted}"
    )

    print("=" * 60)