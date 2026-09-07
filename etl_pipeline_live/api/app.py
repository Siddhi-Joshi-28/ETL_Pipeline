from flask import Flask, jsonify
from datetime import datetime
import random


app = Flask(__name__)


# ============================================================
# ORDER ID MANAGEMENT
# ============================================================

ORDER_ID_FILE = "api/order_id.txt"


def get_next_order_id():

    try:

        with open(
            ORDER_ID_FILE,
            "r"
        ) as file:

            last_id = int(
                file.read().strip()
            )

    except (
        FileNotFoundError,
        ValueError
    ):

        last_id = 100000

    next_id = last_id + 1

    with open(
        ORDER_ID_FILE,
        "w"
    ) as file:

        file.write(
            str(next_id)
        )

    return next_id


# ============================================================
# MASTER DATA
# ============================================================

CITIES = [
    "Ahmedabad",
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Pune",
    "Chennai",
    "Hyderabad",
    "Jaipur",
]


RESTAURANT_CATEGORIES = [
    "Pizza",
    "Indian",
    "Chinese",
    "Fast Food",
    "South Indian",
    "Desserts",
    "Biryani",
]


ORDER_STATUSES = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Cancelled",
    "Pending",
]


PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Wallet",
]


DELIVERY_TYPES = [
    "Normal",
    "Express",
]


# ============================================================
# GENERATE ONE NORMAL ORDER
# ============================================================

def generate_order(order_id):

    item_count = random.randint(
        1,
        6
    )

    order_amount = round(
        random.uniform(
            150,
            2000
        ),
        2
    )

    discount = round(
        random.uniform(
            0,
            200
        ),
        2
    )

    delivery_fee = round(
        random.uniform(
            20,
            80
        ),
        2
    )

    order_status = random.choice(
        ORDER_STATUSES
    )

    # Delivered orders get
    # delivery time and rating.

    if order_status == "Delivered":

        delivery_time = random.randint(
            20,
            60
        )

        rating = round(
            random.uniform(
                1,
                5
            ),
            1
        )

    else:

        delivery_time = None
        rating = None

    order = {

        "order_id": order_id,

        "customer_id": random.randint(
            1000,
            1100
        ),

        "restaurant_id": random.randint(
            100,
            150
        ),

        "order_timestamp": (
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ),

        "city": random.choice(
            CITIES
        ),

        "restaurant_category": random.choice(
            RESTAURANT_CATEGORIES
        ),

        "order_status": order_status,

        "payment_method": random.choice(
            PAYMENT_METHODS
        ),

        "delivery_type": random.choice(
            DELIVERY_TYPES
        ),

        "item_count": item_count,

        "order_amount": order_amount,

        "discount": discount,

        "delivery_fee": delivery_fee,

        "rating": rating,

        "delivery_time_minutes": delivery_time
    }

    return order


# ============================================================
# ADD BAD DATA FOR ETL PRACTICE
# ============================================================

def introduce_bad_data(orders):

    if not orders:
        return orders

    # --------------------------------------------------------
    # 1. CREATE DUPLICATE
    # --------------------------------------------------------

    if len(orders) >= 5:

        duplicate_index = random.randint(
            0,
            len(orders) - 1
        )

        duplicate_order = orders[
            duplicate_index
        ].copy()

        orders.append(
            duplicate_order
        )


    # --------------------------------------------------------
    # 2. CREATE INVALID ORDER
    # --------------------------------------------------------

    if len(orders) >= 4:

        bad_order = orders[
            random.randint(
                0,
                len(orders) - 1
            )
        ].copy()

        # Keep same order_id so that
        # validation can detect it as
        # duplicate in some cases.

        bad_order["order_id"] = (
            get_next_order_id()
        )

        # Randomly introduce one
        # invalid field.

        bad_type = random.choice([

            "negative_amount",

            "zero_items",

            "invalid_status",

            "invalid_payment",

            "invalid_rating",

            "negative_delivery_fee",

            "invalid_delivery_time",

            "missing_city",

            "missing_customer"

        ])


        if bad_type == "negative_amount":

            bad_order["order_amount"] = -500


        elif bad_type == "zero_items":

            bad_order["item_count"] = 0


        elif bad_type == "invalid_status":

            bad_order["order_status"] = "Unknown"


        elif bad_type == "invalid_payment":

            bad_order["payment_method"] = "Bitcoin"


        elif bad_type == "invalid_rating":

            bad_order["rating"] = 10


        elif bad_type == "negative_delivery_fee":

            bad_order["delivery_fee"] = -50


        elif bad_type == "invalid_delivery_time":

            bad_order["delivery_time_minutes"] = 0


        elif bad_type == "missing_city":

            bad_order["city"] = None


        elif bad_type == "missing_customer":

            bad_order["customer_id"] = None


        orders.append(
            bad_order
        )


    # --------------------------------------------------------
    # SHUFFLE DATA
    # --------------------------------------------------------

    random.shuffle(
        orders
    )

    return orders


# ============================================================
# HOME ENDPOINT
# ============================================================

@app.route("/")
def home():

    return jsonify({

        "project":
            "Food Delivery Live Data API",

        "status":
            "running",

        "endpoint":
            "/api/orders"
    })


# ============================================================
# ORDERS ENDPOINT
# ============================================================

@app.route("/api/orders")
def get_orders():

    orders = []


    # --------------------------------------------------------
    # RANDOM BATCH SIZE
    # --------------------------------------------------------
    # API will initially generate between
    # 7 and 15 normal records.
    #
    # After bad data is added,
    # final count can be slightly higher.
    # --------------------------------------------------------

    batch_size = random.randint(
        7,
        15
    )


    # --------------------------------------------------------
    # GENERATE NORMAL ORDERS
    # --------------------------------------------------------

    for _ in range(
        batch_size
    ):

        order_id = get_next_order_id()

        order = generate_order(
            order_id
        )

        orders.append(
            order
        )


    # --------------------------------------------------------
    # ADD DUPLICATES + INVALID DATA
    # --------------------------------------------------------

    orders = introduce_bad_data(
        orders
    )


    # --------------------------------------------------------
    # RETURN API RESPONSE
    # --------------------------------------------------------

    return jsonify({

        "status": "success",

        "count": len(orders),

        "orders": orders
    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )