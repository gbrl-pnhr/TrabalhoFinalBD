import logging
from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from packages.common.src.models.menu_models import DishCreate, DishResponse, DishUpdate
from apps.api.modules.menu.repository import MenuRepository

router = APIRouter(prefix="/menu", tags=["Menu"])
logger = logging.getLogger(__name__)

async def get_db_connection(request: Request):
    async with request.app.state.pool.connection() as conn:
        yield conn

def get_repository(conn = Depends(get_db_connection)):
    return MenuRepository(conn)

@router.get("/categories", response_model=List[str])
async def list_categories(repo: MenuRepository = Depends(get_repository)):
    """
    Get distinct categories available in the menu.
    """
    try:
        return await repo.get_categories()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.get("/dishes", response_model=List[DishResponse])
async def list_dishes(repo: MenuRepository = Depends(get_repository)):
    """
    Get all available dishes in the menu.
    """
    try:
        return await repo.get_all_dishes()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching dishes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.post("/dishes", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(dish: DishCreate, repo: MenuRepository = Depends(get_repository)):
    """
    Add a new dish to the menu.
    """
    try:
        return await repo.create_dish(dish)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error creating dish: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.patch("/dishes/{dish_id}", response_model=DishResponse)
async def update_dish(
    dish_id: int,
    dish_update: DishUpdate,
    repo: MenuRepository = Depends(get_repository)
):
    """
    Update dish details (Price, Name, or Category).
    """
    try:
        updated_dish = await repo.update_dish(dish_id, dish_update)
        if not updated_dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dish not found."
            )
        return updated_dish
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating dish: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

@router.delete("/dishes/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(dish_id: int, repo: MenuRepository = Depends(get_repository)):
    """
    Remove a dish from the menu.
    """
    try:
        success = await repo.delete_dish(dish_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found."
            )
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting dish: {e}")
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete dish because it is part of existing orders.",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )