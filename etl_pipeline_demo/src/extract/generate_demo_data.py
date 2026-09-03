import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Output file
OUTPUT_FILE = RAW_DATA_DIR / "helloq_questions_raw.csv"


CATEGORIES = [
    "Technology",
    "Education",
    "Career",
    "Health",
    "Business",
    "Programming",
    "General",
]

CITIES = [
    "Ahmedabad",
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Pune",
    "Chennai",
    "Hyderabad",
    "Jaipur",
]

QUESTIONS = [
    "How can I learn Python?",
    "How can I improve my programming skills?",
    "What is the best way to learn SQL?",
    "How can I prepare for a technical interview?",
    "What is data engineering?",
    "How can I start learning machine learning?",
    "What are good resources for learning technology?",
    "How can I improve my career skills?",
    "What is the difference between SQL and NoSQL?",
    "How can I learn data analytics?",
]


def generate_questions(number_of_records=100):
    """
    Generate demo HelloQ question data.
    """

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    start_date = datetime(2026, 1, 1)

    rows = []

    for i in range(1, number_of_records + 1):

        user_id = random.randint(1, 30)

        question_id = i

        category = random.choice(CATEGORIES)

        city = random.choice(CITIES)

        question_text = random.choice(QUESTIONS)

        created_at = start_date + timedelta(
            minutes=random.randint(0, 60 * 24 * 180)
        )

        rows.append(
            {
                "question_id": question_id,
                "user_id": user_id,
                "category": category,
                "city": city,
                "question_text": question_text,
                "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        fieldnames = [
            "question_id",
            "user_id",
            "category",
            "city",
            "question_text",
            "created_at",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

    print("=" * 50)
    print("HelloQ demo data generated successfully")
    print("=" * 50)
    print(f"Records created : {number_of_records}")
    print(f"Output file     : {OUTPUT_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    generate_questions(1000)