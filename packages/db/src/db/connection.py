import logging
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from .config import settings

logger = logging.getLogger(__name__)

def create_db_pool() -> ConnectionPool:
    """
    Creates and returns a psycopg ConnectionPool.
    Framework agnostic.
    """
    try:
        new_pool = ConnectionPool(
            conninfo=settings.database_url,
            min_size=1,
            max_size=20,
            kwargs={
                "row_factory": dict_row,
                "autocommit": False,
            },
            open=True,
            name="shared_pool",
        )
        logger.info("Database connection pool created successfully.")
        return new_pool
    except Exception as e:
        logger.error(f"Failed to create database pool: {e}")
        raise