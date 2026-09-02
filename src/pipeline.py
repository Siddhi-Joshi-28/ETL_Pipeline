from src.extract.extract import extract_data
from src.validation.validate import validate_data
from src.cleaning.clean import clean_data
from src.transformation.transform import transform_data
from src.load.load_to_postgres import load_data
from src.logging_config import get_logger


logger = get_logger(__name__)


def run_pipeline():
    """
    Run the complete HelloQ ETL pipeline.

    Pipeline:
    Extract → Validate → Clean → Transform → Load
    """

    logger.info("=" * 60)
    logger.info("HELLOQ ETL PIPELINE STARTED")
    logger.info("=" * 60)

    try:

        # -------------------------------------------------
        # STEP 1: Extract
        # -------------------------------------------------

        logger.info("STEP 1: Starting extraction")

        raw_df = extract_data()

        logger.info(
            f"STEP 1 completed | Records extracted: {len(raw_df)}"
        )

        # -------------------------------------------------
        # STEP 2: Validation
        # -------------------------------------------------

        logger.info("STEP 2: Starting validation")

        valid_df, invalid_df = validate_data(raw_df)

        logger.info(
            f"STEP 2 completed | "
            f"Valid: {len(valid_df)} | "
            f"Invalid: {len(invalid_df)}"
        )

        # -------------------------------------------------
        # STEP 3: Cleaning
        # -------------------------------------------------

        logger.info("STEP 3: Starting cleaning")

        clean_df = clean_data(valid_df)

        logger.info(
            f"STEP 3 completed | "
            f"Clean records: {len(clean_df)}"
        )

        # -------------------------------------------------
        # STEP 4: Transformation
        # -------------------------------------------------

        logger.info("STEP 4: Starting transformation")

        transformed_df = transform_data(clean_df)

        logger.info(
            f"STEP 4 completed | "
            f"Transformed records: {len(transformed_df)}"
        )

        # -------------------------------------------------
        # STEP 5: PostgreSQL Load
        # -------------------------------------------------

        logger.info("STEP 5: Starting PostgreSQL load")

        load_data()

        logger.info("STEP 5 completed | Data loaded successfully")

        # -------------------------------------------------
        # Pipeline completed
        # -------------------------------------------------

        logger.info("=" * 60)
        logger.info("HELLOQ ETL PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)

        print("\n" + "=" * 60)
        print("HELLOQ ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as error:

        logger.error(
            f"ETL PIPELINE FAILED: {error}"
        )

        logger.info("=" * 60)
        logger.info("HELLOQ ETL PIPELINE FAILED")
        logger.info("=" * 60)

        print("\n" + "=" * 60)
        print("HELLOQ ETL PIPELINE FAILED")
        print(f"Error: {error}")
        print("=" * 60)

        raise


if __name__ == "__main__":
    run_pipeline()