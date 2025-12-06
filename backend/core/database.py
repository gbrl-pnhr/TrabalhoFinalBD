import logging
from typing import Generator
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from fastapi import Request
from backend.core.config import settings

logger = logging.getLogger(__name__)


def create_pool() -> ConnectionPool:
    """
    Creates and returns a psycopg ConnectionPool.
    This is a factory function, not a global executor.
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
            name="api_pool",
        )
        logger.info("Database connection pool created successfully.")
        return new_pool
    except Exception as e:
        logger.error(f"Failed to create database pool: {e}")
        raise


def get_db_connection(request: Request) -> Generator[psycopg.Connection, None, None]:
    """
    FastAPI Dependency to yield a database connection from the APP STATE pool.

    This replaces the global variable usage.
    """
    pool: ConnectionPool = request.app.state.pool

    with pool.connection() as conn:
        try:
            yield conn
        except Exception as e:
            logger.error(f"Database transaction error: {e}")
            conn.rollback()
            raise e