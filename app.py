import os
from pathlib import Path

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv


# =====================================================
# PROJECT CONFIGURATION
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(PROJECT_ROOT / ".env")


# =====================================================
# STREAMLIT PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="HelloQ Data Analytics",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    """
    Create a PostgreSQL database connection.
    """

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


# =====================================================
# LOAD QUESTIONS FROM DATABASE
# =====================================================

@st.cache_data
def load_questions():

    connection = get_connection()

    try:

        query = """
        SELECT
            question_id,
            user_id,
            category,
            city,
            question_text,
            created_at,
            created_date,
            created_month,
            created_year,
            processed_at
        FROM questions
        ORDER BY created_at DESC;
        """

        df = pd.read_sql_query(
            query,
            connection
        )

        return df

    finally:

        connection.close()


# =====================================================
# LOAD USER COUNT
# =====================================================

@st.cache_data
def load_user_count():

    connection = get_connection()

    try:

        query = """
        SELECT COUNT(*) AS total_users
        FROM users;
        """

        result = pd.read_sql_query(
            query,
            connection
        )

        return int(result.iloc[0]["total_users"])

    finally:

        connection.close()


# =====================================================
# DASHBOARD TITLE
# =====================================================

st.title("📊 HelloQ Data Analytics Dashboard")

st.write(
    "Analytics dashboard powered by the HelloQ ETL Pipeline "
    "and PostgreSQL."
)


# =====================================================
# LOAD DATA
# =====================================================

try:

    df = load_questions()
    total_users = load_user_count()

except Exception as error:

    st.error(
        "Unable to connect to PostgreSQL database."
    )

    st.error(str(error))

    st.stop()


# =====================================================
# KPI SECTION
# =====================================================

total_questions = len(df)

total_categories = df["category"].nunique()

total_cities = df["city"].nunique()


st.subheader("Key Metrics")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Questions",
        f"{total_questions:,}"
    )


with col2:

    st.metric(
        "Total Users",
        f"{total_users:,}"
    )


with col3:

    st.metric(
        "Categories",
        f"{total_categories:,}"
    )


with col4:

    st.metric(
        "Cities",
        f"{total_cities:,}"
    )


# =====================================================
# QUESTIONS BY CATEGORY
# =====================================================

st.subheader("Questions by Category")


category_data = (
    df.groupby("category")
    .size()
    .reset_index(name="total_questions")
    .sort_values(
        "total_questions",
        ascending=False
    )
)


st.bar_chart(
    category_data.set_index("category")
)


# =====================================================
# QUESTIONS BY CITY
# =====================================================

st.subheader("Questions by City")


city_data = (
    df.groupby("city")
    .size()
    .reset_index(name="total_questions")
    .sort_values(
        "total_questions",
        ascending=False
    )
)


st.bar_chart(
    city_data.set_index("city")
)


# =====================================================
# QUESTIONS OVER TIME
# =====================================================

st.subheader("Questions Over Time")


monthly_data = (
    df.groupby("created_month")
    .size()
    .reset_index(name="total_questions")
    .sort_values("created_month")
)


st.line_chart(
    monthly_data.set_index("created_month")
)


# =====================================================
# TOP USERS
# =====================================================

st.subheader("Top Users by Questions")


top_users = (
    df.groupby("user_id")
    .size()
    .reset_index(name="total_questions")
    .sort_values(
        "total_questions",
        ascending=False
    )
    .head(10)
)


st.dataframe(
    top_users,
    use_container_width=True
)


# =====================================================
# LATEST QUESTIONS
# =====================================================

st.subheader("Latest Questions")


latest_questions = df[
    [
        "question_id",
        "user_id",
        "category",
        "city",
        "question_text",
        "created_at"
    ]
].head(20)


st.dataframe(
    latest_questions,
    use_container_width=True
)