import psycopg2
import streamlit as st
import plotly.express as px

from dashboard.components import (
    load_css,
    page_header,
    kpi_card,
    section_title,
    chart_card_title,
)

from src.analytics.queries import (
    get_total_orders,
    get_total_revenue,
    get_average_order_value,
    get_cancellation_rate,
    get_average_delivery_time,
    get_orders_by_city,
    get_revenue_by_city,
    get_orders_by_category,
    get_orders_by_hour,
    get_order_status,
    get_payment_methods,
    get_delivery_type,
)


load_css()

page_header(
    "Food Delivery Analytics",
    "Real-time operational and business overview",
)

if st.button("Refresh Data", use_container_width=False):
    st.rerun()


# --------------------------------------------------
# Load KPIs
# --------------------------------------------------

try:
    total_orders = get_total_orders()
    total_revenue = get_total_revenue()
    average_order_value = get_average_order_value()
    cancellation_rate = get_cancellation_rate()
    average_delivery_time = get_average_delivery_time()

except psycopg2.errors.UndefinedTable:
    st.error(
        "The **orders** table doesn't exist in your database yet. "
        "Run `sql/schema.sql` against your PostgreSQL database, then load data "
        "with `python -m src.load.load_postgres`, and refresh this page."
    )
    st.code("psql -U postgres -d food_delivery -f sql/schema.sql", language="bash")
    st.stop()

except psycopg2.OperationalError as error:
    st.error(
        "Can't connect to PostgreSQL. Check that Postgres is running and that "
        "the credentials in your `.env` file (POSTGRES_HOST / PORT / DB / USER / PASSWORD) are correct."
    )
    st.exception(error)
    st.stop()

except Exception as error:
    st.error("Something went wrong loading dashboard data.")
    st.exception(error)
    st.stop()


# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

section_title("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    kpi_card("TOTAL ORDERS", f"{total_orders:,}", "Orders processed")

with col2:
    kpi_card("TOTAL REVENUE", f"₹{total_revenue:,.0f}", "Net order revenue")

with col3:
    kpi_card("AVERAGE ORDER", f"₹{average_order_value:,.0f}", "Average order value")

with col4:
    kpi_card("CANCELLATION", f"{cancellation_rate:.1f}%", "Cancelled orders")

with col5:
    kpi_card("AVG DELIVERY", f"{average_delivery_time:.1f} min", "Average delivery time")


# --------------------------------------------------
# City section
# --------------------------------------------------

section_title("Orders & Revenue by City")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        chart_card_title("Orders by City")
        city_df = get_orders_by_city()
        fig = px.bar(city_df, x="city", y="total_orders", text="total_orders")
        fig.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    with st.container(border=True):
        chart_card_title("Revenue by City")
        revenue_city_df = get_revenue_by_city()
        fig = px.bar(revenue_city_df, x="city", y="total_revenue", text="total_revenue")
        fig.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# Category and Status
# --------------------------------------------------

section_title("Orders Overview")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        chart_card_title("Restaurant Categories")
        category_df = get_orders_by_category()
        fig = px.pie(category_df, names="restaurant_category", values="total_orders", hole=0.45)
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

with col2:
    with st.container(border=True):
        chart_card_title("Order Status")
        status_df = get_order_status()
        fig = px.pie(status_df, names="order_status", values="total_orders", hole=0.45)
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

with col3:
    with st.container(border=True):
        chart_card_title("Payment Methods")
        payment_df = get_payment_methods()
        fig = px.pie(payment_df, names="payment_method", values="total_orders", hole=0.45)
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# Time analysis
# --------------------------------------------------

section_title("Order Activity")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        chart_card_title("Orders by Hour")
        hour_df = get_orders_by_hour()
        fig = px.line(hour_df, x="order_hour", y="total_orders", markers=True)
        fig.update_layout(
            xaxis_title="Hour", yaxis_title="Orders",
            height=340, margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    with st.container(border=True):
        chart_card_title("Orders by Delivery Type")
        delivery_type_df = get_delivery_type()
        fig = px.bar(delivery_type_df, x="delivery_type", y="total_orders", text="total_orders")
        fig.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
