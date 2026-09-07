import logging
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIR / "pipeline.log"


# --------------------------------------------------
# Logger configuration
# --------------------------------------------------

logger = logging.getLogger("etl_pipeline")

logger.setLevel(logging.INFO)


# Prevent duplicate handlers
if not logger.handlers:

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    # Console handler
    console_handler = logging.StreamHandler()


    # Log format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    console_handler.setFormatter(
        formatter
    )


    # Add handlers
    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )