import logging
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from apps.api.core.database import get_db_connection
from apps.api.modules.customers.models import CustomerCreate, CustomerResponse
from apps.api.modules.customers.repository import CustomerRepository

router = APIRouter(prefix="/customers", tags=["Customers"])
logger = logging.getLogger(__name__)


def get_repository(conn=Depends(get_db_connection)):
    """Dependency to provide the CustomerRepository."""
    return CustomerRepository(conn)


@router.get("/", response_model=List[CustomerResponse])
def list_customers(repo: CustomerRepository = Depends(get_repository)):
    """
    Get all registered customers.
    """
    try:
        return repo.get_all_customers()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: CustomerCreate, repo: CustomerRepository = Depends(get_repository)
):
    """
    Register a new customer.
    """
    try:
        return repo.create_customer(customer)
    except HTTPException as e:
        raise e
    except Exception as e:
        if "23505" in str(e) or "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Customer with this email already exists.",
            )
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )