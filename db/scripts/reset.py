import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import logging
from dotenv import load_dotenv
from yoyo import read_migrations, get_backend
from backend.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("db_reset")
load_dotenv()


def get_db_url():
    """Constructs the DB URL safely from .env"""
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    if not all([user, password, host, port, dbname]):
        logger.critical("Missing database credentials in .env file")
        sys.exit(1)
    logger.debug(f"Connecting to database at {host}:{port}/{dbname}")
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def reset_database():
    logger.info("Starting database reset process...")
    db_url = get_db_url()
    try:
        backend = get_backend(db_url)
        migrations_dir = os.path.join(os.path.dirname(__file__), "../migrations")
        migrations = read_migrations(migrations_dir)
        logger.info("Checking for applied migrations to rollback...")
        to_rollback = backend.to_rollback(migrations)
        if to_rollback:
            logger.info(f"Rolling back {len(to_rollback)} migrations. This will destroy data.")
            backend.rollback_migrations(to_rollback)
            logger.info("Rollback complete.")
        else:
            logger.info("No migrations found to rollback. Database is clean.")
        logger.info("Re-applying all migrations...")
        to_apply = backend.to_apply(migrations)
        if to_apply:
            backend.apply_migrations(to_apply)
            logger.info(f"Applied {len(to_apply)} migrations successfully.")
        else:
            logger.info("No migrations to apply.")
        logger.info("Database reset successfully.")

    except Exception as e:
        logger.error(f"Database reset failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    print("\n⚠️  WARNING: This will ROLLBACK all migrations and DELETE ALL DATA. ⚠️")
    confirm = input("Are you sure you want to reset the database? (type 'yes' to confirm): ")

    if confirm.lower() == 'yes':
        reset_database()
    else:
        logger.info("Database reset cancelled by user.")
        print("Operation cancelled.")