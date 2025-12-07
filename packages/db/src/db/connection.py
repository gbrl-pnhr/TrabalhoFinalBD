import logging
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from .config import settings

logger = logging.getLogger(__name__)

async def create_db_pool() -> AsyncConnectionPool:
    """
    Creates and returns a psycopg AsyncConnectionPool.
    Framework agnostic.
    """
    try:
        new_pool = AsyncConnectionPool(
            conninfo=settings.database_url,
            min_size=1,
            max_size=20,
            kwargs={
                "row_factory": dict_row,
                "autocommit": False,
            },
            open=False,
            name="shared_pool",
        )
        await new_pool.open()
        logger.info("Database connection pool created successfully.")
        return new_pool
    except Exception as e:
        logger.error(f"Failed to create database pool: {e}")
        raise