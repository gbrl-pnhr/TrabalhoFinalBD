import logging
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from backend.core.database import get_db_connection
from backend.modules.menu.models import DishCreate, DishResponse
from backend.modules.menu.repository import MenuRepository

router = APIRouter(prefix="/menu", tags=["Menu"])
logger = logging.getLogger(__name__)

def get_repository(conn = Depends(get_db_connection)):
    return MenuRepository(conn)

@router.get("/dishes", response_model=List[DishResponse])
def list_dishes(repo: MenuRepository = Depends(get_repository)):
    """
    Get all available dishes in the menu.
    """
    try:
        return repo.get_all_dishes()
    except Exception as e:
        logger.error(f"Error fetching dishes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.post("/dishes", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
def create_dish(dish: DishCreate, repo: MenuRepository = Depends(get_repository)):
    """
    Add a new dish to the menu.
    """
    try:
        return repo.create_dish(dish)
    except Exception as e:
        logger.error(f"Error fetching dishes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )