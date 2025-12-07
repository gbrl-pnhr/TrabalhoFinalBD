import logging
from typing import Generator
import psycopg
from fastapi import Request
from psycopg_pool import ConnectionPool

logger = logging.getLogger(__name__)


def get_db_connection(request: Request) -> Generator[psycopg.Connection, None, None]:
    """
    FastAPI Dependency to yield a database connection from the APP STATE pool.
    """
    pool: ConnectionPool = request.app.state.pool

    with pool.connection() as conn:
        try:
            yield conn
        except Exception as e:
            logger.error(f"Database transaction error: {e}")
            conn.rollback()
            raise e