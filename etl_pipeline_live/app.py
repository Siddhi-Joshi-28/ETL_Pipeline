import streamlit as st


st.set_page_config(
    page_title="Food Delivery Analytics",
    page_icon="🍔",
    layout="wide"
)


overview = st.Page(
    "dashboard/pages/overview.py",
    title="Dashboard",
    icon="📊",
    default=True,
)

analysis = st.Page(
    "dashboard/pages/analysis.py",
    title="Analysis",
    icon="🔎",
)

orders = st.Page(
    "dashboard/pages/orders.py",
    title="Total Orders",
    icon="🧾",
)


pg = st.navigation([overview, analysis, orders])

pg.run()