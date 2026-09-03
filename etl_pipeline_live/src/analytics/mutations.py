import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


ORDER_COLUMNS = [
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
    "average_item_price",
]


def get_connection():

    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "food_delivery"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def get_next_order_id():
    """Returns the next free order_id (max existing id + 1, or 100001 if empty)."""

    query = "SELECT COALESCE(MAX(order_id), 100000) + 1 AS next_id FROM orders;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()[0]


def insert_order(order):
    """order: dict containing every key in ORDER_COLUMNS. Returns True if inserted."""

    placeholders = ", ".join(["%s"] * len(ORDER_COLUMNS))
    columns_sql = ", ".join(ORDER_COLUMNS)

    query = f"""
        INSERT INTO orders ({columns_sql})
        VALUES ({placeholders})
        ON CONFLICT (order_id) DO NOTHING
        RETURNING order_id;
    """

    values = [order[column] for column in ORDER_COLUMNS]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            result = cur.fetchone()
            conn.commit()

    return result is not None


def delete_order(order_id):
    """Deletes an order by order_id. Returns number of rows deleted (0 or 1)."""

    query = "DELETE FROM orders WHERE order_id = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (order_id,))
            deleted = cur.rowcount
            conn.commit()

    return deleted