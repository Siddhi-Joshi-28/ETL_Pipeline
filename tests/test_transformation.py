import pandas as pd

from src.transformation.transform import transform_data


def test_transformation_creates_date_columns():

    df = pd.DataFrame({
        "question_id": [1],
        "user_id": [10],
        "category": ["Technology"],
        "city": ["Mumbai"],
        "question_text": ["How can I learn Python?"],
        "created_at": ["2026-01-15 10:30:00"]
    })

    transformed_df = transform_data(df)

    assert "created_date" in transformed_df.columns
    assert "created_month" in transformed_df.columns
    assert "created_year" in transformed_df.columns
    assert "processed_at" in transformed_df.columns


def test_transformation_preserves_record_count():

    df = pd.DataFrame({
        "question_id": [1, 2],
        "user_id": [10, 20],
        "category": ["Technology", "Career"],
        "city": ["Mumbai", "Pune"],
        "question_text": [
            "How can I learn Python?",
            "How can I improve my resume?"
        ],
        "created_at": [
            "2026-01-15 10:30:00",
            "2026-02-15 11:30:00"
        ]
    })

    transformed_df = transform_data(df)

    assert len(transformed_df) == len(df)