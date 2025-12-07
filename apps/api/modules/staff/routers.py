import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Request
from packages.common.src.models.waiters_models import WaiterCreate, WaiterResponse
from apps.api.modules.staff.waiters.repository import WaiterRepository
from packages.common.src.models.chef_models import ChefCreate, ChefResponse
from apps.api.modules.staff.chefs.repository import ChefRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/staff", tags=["Staff"])

async def get_db_connection(request: Request):
    async with request.app.state.pool.connection() as conn:
        yield conn

def get_waiter_repo(conn=Depends(get_db_connection)):
    return WaiterRepository(conn)

def get_chef_repo(conn=Depends(get_db_connection)):
    return ChefRepository(conn)

@router.get("/waiters", response_model=List[WaiterResponse])
async def list_waiters(repo: WaiterRepository = Depends(get_waiter_repo)):
    """List all waiters."""
    try:
        return await repo.get_all_waiters()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching waiters: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.delete("/waiters/{waiter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_waiter(waiter_id: int, repo: WaiterRepository = Depends(get_waiter_repo)):
    """Fire/Remove a waiter."""
    try:
        success = await repo.delete_waiter(waiter_id)
        if not success:
            raise HTTPException(status_code=404, detail="Waiter not found.")
    except Exception as e:
        logger.error(f"Error deleting waiter: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/chefs/{chef_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chef(chef_id: int, repo: ChefRepository = Depends(get_chef_repo)):
    """Fire/Remove a chef."""
    try:
        success = await repo.delete_chef(chef_id)
        if not success:
            raise HTTPException(status_code=404, detail="Chef not found.")
    except Exception as e:
        logger.error(f"Error deleting chef: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/waiters", response_model=WaiterResponse, status_code=status.HTTP_201_CREATED)
async def create_waiter(waiter: WaiterCreate, repo: WaiterRepository = Depends(get_waiter_repo)):
    """Register a new waiter."""
    try:
        return await repo.create_waiter(waiter)
    except HTTPException as e:
        raise e
    except Exception as e:
        if "unique constraint" in str(e).lower() and "cpf" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A waiter with this CPF already exists."
            )
        logger.error(f"Error creating waiter: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.get("/chefs", response_model=List[ChefResponse])
async def list_chefs(repo: ChefRepository = Depends(get_chef_repo)):
    """List all chefs."""
    try:
        return await repo.get_all_chefs()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching chefs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.post("/chefs", response_model=ChefResponse, status_code=status.HTTP_201_CREATED)
async def create_chef(chef: ChefCreate, repo: ChefRepository = Depends(get_chef_repo)):
    """Register a new chef."""
    try:
        return await repo.create_chef(chef)
    except HTTPException as e:
        raise e
    except Exception as e:
        if "unique constraint" in str(e).lower() and "cpf" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A chef with this CPF already exists."
            )
        logger.error(f"Error creating chef: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )