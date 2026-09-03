from flask import Flask, jsonify
from datetime import datetime
import random


app = Flask(__name__)

# --------------------------------------------------
# Order ID Management
# --------------------------------------------------

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

# --------------------------------------------------
# Master Data
# --------------------------------------------------

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


# --------------------------------------------------
# Generate One Order
# --------------------------------------------------

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

    # Only delivered orders get
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


# --------------------------------------------------
# Home Endpoint
# --------------------------------------------------

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


# --------------------------------------------------
# Orders Endpoint
# --------------------------------------------------

@app.route("/api/orders")
def get_orders():

    orders = []

    for _ in range(10):

        # Generate a unique order ID
        order_id = get_next_order_id()

        order = generate_order(
            order_id
        )

        orders.append(order)

    return jsonify({

        "status": "success",

        "count": len(orders),

        "orders": orders
    })


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )