from pathlib import Path

from src.extract.extract import extract_data


def test_raw_data_file_exists():

    project_root = Path(__file__).resolve().parents[1]

    raw_file = (
        project_root
        / "data"
        / "raw"
        / "helloq_questions_raw.csv"
    )

    assert raw_file.exists()


def test_extract_returns_data():

    df = extract_data()

    assert df is not None
    assert len(df) > 0


def test_extract_has_required_columns():

    df = extract_data()

    required_columns = [
        "question_id",
        "user_id",
        "category",
        "city",
        "question_text",
        "created_at",
    ]

    for column in required_columns:
        assert column in df.columns