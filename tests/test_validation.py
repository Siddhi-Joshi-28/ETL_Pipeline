import pandas as pd

from src.validation.validate import validate_data


def test_valid_data_passes_validation():

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
            "2026-01-01 10:00:00",
            "2026-01-02 11:00:00"
        ]
    })

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 2
    assert len(invalid_df) == 0


def test_invalid_question_id_is_rejected():

    df = pd.DataFrame({
        "question_id": ["invalid"],
        "user_id": [10],
        "category": ["Technology"],
        "city": ["Mumbai"],
        "question_text": ["How can I learn Python?"],
        "created_at": ["2026-01-01 10:00:00"]
    })

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1


def test_missing_required_value_is_rejected():

    df = pd.DataFrame({
        "question_id": [1],
        "user_id": [10],
        "category": ["Technology"],
        "city": [None],
        "question_text": ["How can I learn Python?"],
        "created_at": ["2026-01-01 10:00:00"]
    })

    valid_df, invalid_df = validate_data(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 1