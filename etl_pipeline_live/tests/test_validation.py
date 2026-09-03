import pandas as pd

from src.validation.validate import (
    validate_orders
)


def create_test_data():

    return pd.DataFrame([

        {
            "order_id": 1,
            "customer_id": 1001,
            "restaurant_id": 101,
            "order_timestamp": "2026-09-03 10:00:00",
            "city": "Ahmedabad",
            "restaurant_category": "Pizza",
            "order_status": "Delivered",
            "payment_method": "UPI",
            "delivery_type": "Normal",
            "item_count": 2,
            "order_amount": 500,
            "discount": 50,
            "delivery_fee": 30,
            "rating": 4.5,
            "delivery_time_minutes": 30
        },

        {
            "order_id": 2,
            "customer_id": 1002,
            "restaurant_id": 102,
            "order_timestamp": "2026-09-03 10:05:00",
            "city": "Mumbai",
            "restaurant_category": "Indian",
            "order_status": "WrongStatus",
            "payment_method": "UPI",
            "delivery_type": "Normal",
            "item_count": 2,
            "order_amount": 600,
            "discount": 50,
            "delivery_fee": 30,
            "rating": 4,
            "delivery_time_minutes": 35
        },

        {
            "order_id": 3,
            "customer_id": 1003,
            "restaurant_id": 103,
            "order_timestamp": "2026-09-03 10:10:00",
            "city": "Delhi",
            "restaurant_category": "Chinese",
            "order_status": "Delivered",
            "payment_method": "UPI",
            "delivery_type": "Normal",
            "item_count": 0,
            "order_amount": -100,
            "discount": 50,
            "delivery_fee": 30,
            "rating": 7,
            "delivery_time_minutes": 40
        }

    ])


def test_validation():

    df = create_test_data()

    valid_df, rejected_df = (
        validate_orders(df)
    )

    assert len(valid_df) == 1

    assert len(rejected_df) == 2


def test_invalid_status():

    df = create_test_data()

    _, rejected_df = validate_orders(df)

    assert any(
        rejected_df[
            "validation_error"
        ].str.contains(
            "Invalid order_status"
        )
    )


def test_invalid_amount():

    df = create_test_data()

    _, rejected_df = validate_orders(df)

    assert any(
        rejected_df[
            "validation_error"
        ].str.contains(
            "order_amount"
        )
    )