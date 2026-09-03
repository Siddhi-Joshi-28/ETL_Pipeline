import os
import pandas as pd
import streamlit as st
import psycopg2
from dotenv import load_dotenv
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent

# Load .env
load_dotenv(PROJECT_ROOT / ".env")


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def get_data(query):
    connection = get_connection()

    try:
        return pd.read_sql(query, connection)
    finally:
        connection.close()


st.set_page_config(
    page_title="HelloQ ETL Dashboard",
    page_icon="📊",
    layout="wide"
)


st.title("📊 HelloQ ETL Dashboard")
st.write("This dashboard displays data directly from PostgreSQL.")


if st.button("🔄 Refresh Data"):
    st.rerun()


# --------------------------------------------------
# KPI DATA
# --------------------------------------------------

total_questions = get_data(
    "SELECT COUNT(*) AS count FROM questions"
).iloc[0]["count"]

total_users = get_data(
    "SELECT COUNT(*) AS count FROM users"
).iloc[0]["count"]

total_categories = get_data(
    "SELECT COUNT(DISTINCT category) AS count FROM questions"
).iloc[0]["count"]

total_cities = get_data(
    "SELECT COUNT(DISTINCT city) AS count FROM questions"
).iloc[0]["count"]


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Questions", total_questions)
col2.metric("Total Users", total_users)
col3.metric("Categories", total_categories)
col4.metric("Cities", total_cities)


st.divider()


# --------------------------------------------------
# QUESTIONS BY CATEGORY
# --------------------------------------------------

st.subheader("📚 Questions by Category")

category_df = get_data("""
    SELECT category, COUNT(*) AS question_count
    FROM questions
    GROUP BY category
    ORDER BY question_count DESC;
""")

st.bar_chart(
    category_df.set_index("category")
)


# --------------------------------------------------
# QUESTIONS BY CITY
# --------------------------------------------------

st.subheader("🏙️ Questions by City")

city_df = get_data("""
    SELECT city, COUNT(*) AS question_count
    FROM questions
    GROUP BY city
    ORDER BY question_count DESC;
""")

st.bar_chart(
    city_df.set_index("city")
)


# --------------------------------------------------
# QUESTIONS BY MONTH
# --------------------------------------------------

st.subheader("📅 Questions by Month")

month_df = get_data("""
    SELECT created_month, COUNT(*) AS question_count
    FROM questions
    GROUP BY created_month
    ORDER BY created_month;
""")

st.line_chart(
    month_df.set_index("created_month")
)


# --------------------------------------------------
# RECENT QUESTIONS
# --------------------------------------------------

st.subheader("📝 Recent Questions")

questions_df = get_data("""
    SELECT
        question_id,
        user_id,
        category,
        city,
        question_text,
        created_at
    FROM questions
    ORDER BY created_at DESC
    LIMIT 20;
""")

st.dataframe(
    questions_df,
    use_container_width=True
)