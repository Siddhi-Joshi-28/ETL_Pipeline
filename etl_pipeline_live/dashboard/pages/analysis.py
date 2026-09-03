import psycopg2
import streamlit as st
import plotly.express as px

from dashboard.components import (
    load_css,
    page_header,
    section_title,
    chart_card_title,
    status_badge,
)

from src.analytics.queries import (
    get_revenue_by_category,
    get_daily_revenue,
    get_delivery_performance,
    get_top_customers,
    get_recent_orders,
)


load_css()

page_header(
    "Analysis",
    "Deeper cuts into revenue, categories, and customer activity",
)


try:
    revenue_category_df = get_revenue_by_category()
    daily_revenue_df = get_daily_revenue()
    delivery_perf_df = get_delivery_performance()
    top_customers_df = get_top_customers()
    recent_orders_df = get_recent_orders(limit=10)

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
        "the credentials in your `.env` file are correct."
    )
    st.exception(error)
    st.stop()

except Exception as error:
    st.error("Something went wrong loading analysis data.")
    st.exception(error)
    st.stop()


# --------------------------------------------------
# Revenue by category
# --------------------------------------------------

section_title("Revenue by Restaurant Category")

col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):
        chart_card_title("Revenue by Category")
        fig = px.bar(
            revenue_category_df.sort_values("total_revenue"),
            x="total_revenue", y="restaurant_category",
            orientation="h", text="total_revenue",
        )
        fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    with st.container(border=True):
        chart_card_title("Average Order Value by Category")
        fig = px.bar(
            revenue_category_df.sort_values("average_order_value"),
            x="average_order_value", y="restaurant_category",
            orientation="h",
        )
        fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# Daily revenue trend
# --------------------------------------------------

section_title("Daily Revenue Trend")

with st.container(border=True):
    chart_card_title("Orders & Revenue Over Time")
    fig = px.area(daily_revenue_df, x="order_date", y="total_revenue")
    fig.update_layout(
        xaxis_title="Date", yaxis_title="Revenue (₹)",
        height=360, margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# Delivery performance + top customers
# --------------------------------------------------

section_title("Delivery Performance & Top Customers")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        chart_card_title("Delivery Performance")
        fig = px.pie(delivery_perf_df, names="delivery_performance", values="total_orders", hole=0.45)
        fig.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

with col2:
    with st.container(border=True):
        chart_card_title("Top 10 Customers by Spend")

        rows_html = "".join(
            f"<tr><td>{row.customer_id}</td><td>{row.total_orders}</td>"
            f"<td>₹{row.total_spent:,.0f}</td></tr>"
            for row in top_customers_df.itertuples()
        )

        st.markdown(
            f"""
            <table class="data-table">
                <tr><th>Customer ID</th><th>Orders</th><th>Total Spent</th></tr>
                {rows_html}
            </table>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# Recent orders
# --------------------------------------------------

section_title("Recent Orders")

with st.container(border=True):
    rows_html = "".join(
        f"<tr><td>{row.order_id}</td><td>{row.order_timestamp}</td>"
        f"<td>{row.city}</td><td>{row.restaurant_category}</td>"
        f"<td>{status_badge(row.order_status)}</td>"
        f"<td>₹{row.net_amount:,.0f}</td>"
        f"<td>{'-' if row.delivery_time_minutes != row.delivery_time_minutes else f'{row.delivery_time_minutes:.0f} min'}</td>"
        f"<td>{row.delivery_performance}</td></tr>"
        for row in recent_orders_df.itertuples()
    )

    st.markdown(
        f"""
        <table class="data-table">
            <tr>
                <th>Order ID</th><th>Time</th><th>City</th><th>Category</th>
                <th>Status</th><th>Amount</th><th>Delivery Time</th><th>Performance</th>
            </tr>
            {rows_html}
        </table>
        """,
        unsafe_allow_html=True,
    )
