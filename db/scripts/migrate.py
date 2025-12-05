import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import logging
from dotenv import load_dotenv
from yoyo import read_migrations, get_backend
from backend.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("db_migration")
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


def apply_migrations():
    logger.info("Starting database migration process...")
    db_url = get_db_url()
    try:
        backend = get_backend(db_url)
        migrations = read_migrations(
            os.path.join(os.path.dirname(__file__), "../migrations")
        )
        to_apply = backend.to_apply(migrations)
        if not to_apply:
            logger.info("Database is already up to date.")
            return
        logger.info(f"Applying {len(to_apply)} migrations...")
        backend.apply_migrations(to_apply)
        logger.info("Migrations applied successfully.")

    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    apply_migrations()