import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from backend.core.database import get_db_connection
from backend.modules.staff.waiters.models import WaiterCreate, WaiterResponse
from backend.modules.staff.waiters.repository import WaiterRepository
from backend.modules.staff.chefs.models import ChefCreate, ChefResponse
from backend.modules.staff.chefs.repository import ChefRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/staff", tags=["Staff"])

def get_waiter_repo(conn=Depends(get_db_connection)):
    return WaiterRepository(conn)

def get_chef_repo(conn=Depends(get_db_connection)):
    return ChefRepository(conn)

@router.get("/waiters", response_model=List[WaiterResponse])
def list_waiters(repo: WaiterRepository = Depends(get_waiter_repo)):
    """List all waiters."""
    try:
        return repo.get_all_waiters()
    except Exception as e:
        logger.error(f"Error fetching waiters: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.post("/waiters", response_model=WaiterResponse, status_code=status.HTTP_201_CREATED)
def create_waiter(waiter: WaiterCreate, repo: WaiterRepository = Depends(get_waiter_repo)):
    """Register a new waiter."""
    try:
        return repo.create_waiter(waiter)
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
def list_chefs(repo: ChefRepository = Depends(get_chef_repo)):
    """List all chefs."""
    try:
        return repo.get_all_chefs()
    except Exception as e:
        logger.error(f"Error fetching chefs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

@router.post("/chefs", response_model=ChefResponse, status_code=status.HTTP_201_CREATED)
def create_chef(chef: ChefCreate, repo: ChefRepository = Depends(get_chef_repo)):
    """Register a new chef."""
    try:
        return repo.create_chef(chef)
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