import pandas as pd

from src.cleaning.clean import clean_data


def test_duplicate_question_ids_are_removed():

    df = pd.DataFrame({
        "question_id": [1, 1, 2],
        "user_id": [10, 10, 20],
        "category": ["technology", "technology", "career"],
        "city": ["mumbai", "mumbai", "pune"],
        "question_text": [
            "  How can I learn Python?  ",
            "  How can I learn Python?  ",
            "How can I improve my resume?"
        ],
        "created_at": [
            "2026-01-01 10:00:00",
            "2026-01-01 10:00:00",
            "2026-01-02 11:00:00"
        ]
    })

    clean_df = clean_data(df)

    assert len(clean_df) == 2


def test_category_is_standardized():

    df = pd.DataFrame({
        "question_id": [1],
        "user_id": [10],
        "category": ["  technology  "],
        "city": ["  mumbai  "],
        "question_text": ["How can I learn Python?"],
        "created_at": ["2026-01-01 10:00:00"]
    })

    clean_df = clean_data(df)

    assert clean_df.iloc[0]["category"] == "Technology"
    assert clean_df.iloc[0]["city"] == "Mumbai"


def test_question_text_spaces_are_cleaned():

    df = pd.DataFrame({
        "question_id": [1],
        "user_id": [10],
        "category": ["Technology"],
        "city": ["Mumbai"],
        "question_text": [
            "   How     can    I   learn   Python?   "
        ],
        "created_at": ["2026-01-01 10:00:00"]
    })

    clean_df = clean_data(df)

    assert (
        clean_df.iloc[0]["question_text"]
        == "How can I learn Python?"
    )