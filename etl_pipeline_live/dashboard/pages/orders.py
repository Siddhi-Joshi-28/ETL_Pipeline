from datetime import datetime

import psycopg2
import streamlit as st

from dashboard.components import (
    load_css,
    page_header,
    section_title,
    kpi_card,
)

from src.analytics.queries import get_all_orders

from src.analytics.mutations import (
    get_next_order_id,
    insert_order,
    delete_order,
)


load_css()

page_header(
    "Total Orders",
    "Browse every order, export to CSV, or add / remove a record",
)


try:
    orders_df = get_all_orders()

except psycopg2.errors.UndefinedTable:
    st.error(
        "The **orders** table doesn't exist in your database yet. "
        "Run `sql/schema.sql` against your PostgreSQL database, then refresh this page."
    )
    st.code("psql -U postgres -d food_delivery -f sql/schema.sql", language="bash")
    st.stop()

except psycopg2.OperationalError as error:
    st.error(
        "Can't connect to PostgreSQL. Check that Postgres is running and that "
        "the credentials in your `.env` file are correct."
    )
    st.exception(error)
    st.stop()

except Exception as error:
    st.error("Something went wrong loading orders.")
    st.exception(error)
    st.stop()


# --------------------------------------------------
# Total + download
# --------------------------------------------------

section_title("All Orders")

col1, col2 = st.columns([1, 3])

with col1:
    kpi_card("TOTAL ORDERS", f"{len(orders_df):,}", "Rows in the orders table")

with col2:
    st.write("")
    st.download_button(
        label="Download as CSV",
        data=orders_df.to_csv(index=False).encode("utf-8"),
        file_name=f"orders_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=False,
    )

st.dataframe(orders_df, use_container_width=True, height=420)


# --------------------------------------------------
# Add a new order
# --------------------------------------------------

section_title("Add a New Order")

with st.expander("Add order", expanded=False):

    with st.form("add_order_form", clear_on_submit=True):

        col1, col2, col3 = st.columns(3)

        with col1:
            customer_id = st.number_input("Customer ID", min_value=1000, max_value=1100, value=1000)
            restaurant_id = st.number_input("Restaurant ID", min_value=100, max_value=150, value=100)
            city = st.selectbox(
                "City",
                ["Ahmedabad", "Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Hyderabad", "Jaipur"],
            )

        with col2:
            restaurant_category = st.selectbox(
                "Restaurant Category",
                ["Pizza", "Indian", "Chinese", "Fast Food", "South Indian", "Desserts", "Biryani"],
            )
            order_status = st.selectbox("Order Status", ["Delivered", "Cancelled", "Pending"])
            payment_method = st.selectbox(
                "Payment Method", ["UPI", "Credit Card", "Debit Card", "Cash", "Wallet"]
            )
            delivery_type = st.selectbox("Delivery Type", ["Normal", "Express"])

        with col3:
            item_count = st.number_input("Item Count", min_value=1, max_value=20, value=2)
            order_amount = st.number_input("Order Amount", min_value=0.0, value=500.0, step=10.0)
            discount = st.number_input("Discount", min_value=0.0, value=0.0, step=10.0)
            delivery_fee = st.number_input("Delivery Fee", min_value=0.0, value=40.0, step=5.0)
            rating = st.slider("Rating", 1.0, 5.0, 4.0, 0.1)
            delivery_time_minutes = st.number_input(
                "Delivery Time (minutes)", min_value=0, value=30
            )

        submitted = st.form_submit_button("Add Order")

        if submitted:

            now = datetime.now()

            net_amount = order_amount - discount + delivery_fee
            discount_percentage = (discount / order_amount * 100) if order_amount else 0
            average_item_price = order_amount / item_count if item_count else 0

            delivered = order_status == "Delivered"

            if not delivered:
                delivery_time_value = None
            else:
                delivery_time_value = delivery_time_minutes

            if delivery_time_value is None:
                delivery_performance = "Unknown"
            elif delivery_time_value <= 30:
                delivery_performance = "Fast"
            elif delivery_time_value <= 60:
                delivery_performance = "Normal"
            else:
                delivery_performance = "Slow"

            new_order = {
                "order_id": get_next_order_id(),
                "customer_id": customer_id,
                "restaurant_id": restaurant_id,
                "order_timestamp": now,
                "city": city,
                "restaurant_category": restaurant_category,
                "order_status": order_status,
                "payment_method": payment_method,
                "delivery_type": delivery_type,
                "item_count": item_count,
                "order_amount": order_amount,
                "discount": discount,
                "delivery_fee": delivery_fee,
                "rating": rating if delivered else None,
                "delivery_time_minutes": delivery_time_value,
                "net_amount": net_amount,
                "discount_percentage": discount_percentage,
                "order_date": now.date(),
                "order_year": now.year,
                "order_month": now.month,
                "order_month_name": now.strftime("%B"),
                "order_hour": now.hour,
                "order_day": now.strftime("%A"),
                "is_delivered": int(order_status == "Delivered"),
                "is_cancelled": int(order_status == "Cancelled"),
                "is_pending": int(order_status == "Pending"),
                "delivery_performance": delivery_performance,
                "average_item_price": average_item_price,
            }

            success = insert_order(new_order)

            if success:
                st.success(f"Order {new_order['order_id']} added.")
                st.rerun()
            else:
                st.error("Could not add the order (id already existed). Try again.")


# --------------------------------------------------
# Delete an order
# --------------------------------------------------

section_title("Delete an Order")

with st.expander("Delete order", expanded=False):

    if orders_df.empty:
        st.info("No orders to delete.")
    else:
        order_id_to_delete = st.selectbox(
            "Select Order ID to delete",
            orders_df["order_id"].tolist(),
        )

        if st.button("Delete Order", type="primary"):
            deleted_count = delete_order(order_id_to_delete)

            if deleted_count:
                st.success(f"Order {order_id_to_delete} deleted.")
                st.rerun()
            else:
                st.warning("That order was not found (may already be deleted).")