import logging
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from apps.api.core.database import get_db_connection
from apps.api.modules.tables.models import TableCreate, TableResponse
from apps.api.modules.tables.repository import TableRepository

router = APIRouter(prefix="/tables", tags=["Tables"])
logger = logging.getLogger(__name__)


def get_repository(conn=Depends(get_db_connection)):
    """Dependency to provide the TableRepository."""
    return TableRepository(conn)


@router.get("/", response_model=List[TableResponse])
def list_tables(repo: TableRepository = Depends(get_repository)):
    """
    Get all registered tables.
    """
    try:
        return repo.get_all_tables()
    except Exception as e:
        logger.error(f"Error fetching tables: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(
    table: TableCreate, repo: TableRepository = Depends(get_repository)
):
    """
    Register a new table.
    """
    try:
        return repo.create_table(table)
    except Exception as e:
        if "23505" in str(e) or "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Table number {table.number} already exists.",
            )

        logger.error(f"Error creating table: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )