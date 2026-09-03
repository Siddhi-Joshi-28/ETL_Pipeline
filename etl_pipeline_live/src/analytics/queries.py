import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv


# --------------------------------------------------
# Project configuration
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
# PostgreSQL connection
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
# All orders
# --------------------------------------------------

def get_all_orders():

    query = """
        SELECT *
        FROM orders
        ORDER BY order_timestamp DESC;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )

# --------------------------------------------------
# Total orders
# --------------------------------------------------

def get_total_orders():

    query = """
        SELECT COUNT(*) AS total_orders
        FROM orders;
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn
        )

    return int(
        df.iloc[0]["total_orders"]
    )


# --------------------------------------------------
# Total revenue
# --------------------------------------------------

def get_total_revenue():

    query = """
        SELECT
            COALESCE(
                SUM(net_amount),
                0
            ) AS total_revenue
        FROM orders;
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn
        )

    return float(
        df.iloc[0]["total_revenue"]
    )


# --------------------------------------------------
# Average order value
# --------------------------------------------------

def get_average_order_value():

    query = """
        SELECT
            COALESCE(
                AVG(net_amount),
                0
            ) AS average_order_value
        FROM orders;
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn
        )

    return float(
        df.iloc[0]["average_order_value"]
    )


# --------------------------------------------------
# Cancellation rate
# --------------------------------------------------

def get_cancellation_rate():

    query = """
        SELECT
            CASE
                WHEN COUNT(*) = 0 THEN 0
                ELSE
                    100.0 *
                    SUM(
                        CASE
                            WHEN is_cancelled = 1
                            THEN 1
                            ELSE 0
                        END
                    )
                    / COUNT(*)
            END AS cancellation_rate
        FROM orders;
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn
        )

    return float(
        df.iloc[0]["cancellation_rate"]
    )


# --------------------------------------------------
# Orders by city
# --------------------------------------------------

def get_orders_by_city():

    query = """
        SELECT
            city,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY city
        ORDER BY total_orders DESC;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


# --------------------------------------------------
# Revenue by city
# --------------------------------------------------

def get_revenue_by_city():

    query = """
        SELECT
            city,
            ROUND(
                SUM(net_amount),
                2
            ) AS total_revenue
        FROM orders
        GROUP BY city
        ORDER BY total_revenue DESC;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


# --------------------------------------------------
# Orders by restaurant category
# --------------------------------------------------

def get_orders_by_category():

    query = """
        SELECT
            restaurant_category,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY restaurant_category
        ORDER BY total_orders DESC;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


# --------------------------------------------------
# Revenue by restaurant category
# --------------------------------------------------

def get_revenue_by_category():

    query = """
        SELECT
            restaurant_category,
            COUNT(*) AS total_orders,
            ROUND(
                SUM(net_amount),
                2
            ) AS total_revenue,
            ROUND(
                AVG(net_amount),
                2
            ) AS average_order_value
        FROM orders
        GROUP BY restaurant_category
        ORDER BY total_revenue DESC;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


# --------------------------------------------------
# Orders by hour
# --------------------------------------------------

def get_orders_by_hour():

    query = """
        SELECT
            order_hour,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY order_hour
        ORDER BY order_hour;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


# --------------------------------------------------
# Delivery performance
# --------------------------------------------------

def get_delivery_performance():

    query = """
        SELECT
            delivery_performance,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY delivery_performance
        ORDER BY total_orders DESC;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


# --------------------------------------------------
# Order status
# --------------------------------------------------

def get_order_status():

    query = """
        SELECT
            order_status,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY order_status
        ORDER BY total_orders DESC;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


# --------------------------------------------------
# Top customers
# --------------------------------------------------

def get_top_customers():

    query = """
        SELECT
            customer_id,
            COUNT(*) AS total_orders,
            ROUND(
                SUM(net_amount),
                2
            ) AS total_spent
        FROM orders
        GROUP BY customer_id
        ORDER BY total_spent DESC
        LIMIT 10;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


# --------------------------------------------------
# Daily revenue
# --------------------------------------------------

def get_daily_revenue():

    query = """
        SELECT
            order_date,
            COUNT(*) AS total_orders,
            ROUND(
                SUM(net_amount),
                2
            ) AS total_revenue
        FROM orders
        GROUP BY order_date
        ORDER BY order_date;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


def get_payment_methods():

    query = """
        SELECT
            payment_method,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY payment_method
        ORDER BY total_orders DESC;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


def get_delivery_type():

    query = """
        SELECT
            delivery_type,
            COUNT(*) AS total_orders
        FROM orders
        GROUP BY delivery_type
        ORDER BY total_orders DESC;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn
        )


def get_average_delivery_time():

    query = """
        SELECT
            COALESCE(
                AVG(delivery_time_minutes),
                0
            ) AS average_delivery_time
        FROM orders
        WHERE delivery_time_minutes IS NOT NULL;
    """

    with get_connection() as conn:

        df = pd.read_sql_query(
            query,
            conn
        )

    return float(
        df.iloc[0]["average_delivery_time"]
    )


def get_recent_orders(limit=10):

    query = """
        SELECT
            order_id,
            order_timestamp,
            city,
            restaurant_category,
            order_status,
            net_amount,
            delivery_time_minutes,
            delivery_performance
        FROM orders
        ORDER BY order_timestamp DESC
        LIMIT %s;
    """

    with get_connection() as conn:

        return pd.read_sql_query(
            query,
            conn,
            params=(limit,)
        )

# --------------------------------------------------
# Test analytics
# --------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("FOOD DELIVERY ANALYTICS")
    print("=" * 60)

    print()
    print(
        "Total orders:",
        get_total_orders()
    )

    print(
        "Total revenue:",
        get_total_revenue()
    )

    print(
        "Average order value:",
        get_average_order_value()
    )

    print(
        "Cancellation rate:",
        get_cancellation_rate()
    )

    print()
    print("Orders by city:")
    print(
        get_orders_by_city()
        .to_string(index=False)
    )

    print()
    print("Revenue by city:")
    print(
        get_revenue_by_city()
        .to_string(index=False)
    )

    print()
    print("Orders by category:")
    print(
        get_orders_by_category()
        .to_string(index=False)
    )

    print()
    print("Orders by hour:")
    print(
        get_orders_by_hour()
        .to_string(index=False)
    )

    print()
    print("Delivery performance:")
    print(
        get_delivery_performance()
        .to_string(index=False)
    )

    print()
    print("=" * 60)