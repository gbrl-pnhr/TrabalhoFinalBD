import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from typing import Generator
import logging

from backend.core.config import settings

logger = logging.getLogger("api.database")


@contextmanager
def get_db_connection() -> Generator[psycopg.Connection, None, None]:
    """
    Context manager for PostgreSQL database connections.

    Yields:
        psycopg.Connection: A database connection with dict_row factory enabled.

    Raises:
        Exception: Propagates database errors after logging.
    """
    conn = None
    try:
        conn = psycopg.connect(
            conninfo=settings.DATABASE_URL,
            row_factory=dict_row,
            autocommit=False,
        )
        yield conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()