import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from backend.core.database import get_db_connection
from backend.modules.orders.models import OrderCreate, OrderResponse, OrderItemCreate
from backend.modules.orders.service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])
logger = logging.getLogger(__name__)


def get_service(conn=Depends(get_db_connection)):
    """Dependency injection for OrderService."""
    return OrderService(conn)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate, service: OrderService = Depends(get_service)
):
    """
    Open a new order (Table Check-in).
    """
    try:
        return service.create_order(order_data)
    except Exception as e:
        logger.error(f"API Error create_order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order."
        )


@router.get("/", response_model=List[OrderResponse])
def list_orders(service: OrderService = Depends(get_service)):
    """
    List all active orders.
    """
    try:
        return service.list_orders()
    except Exception as e:
        logger.error(f"API Error list_orders: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch orders."
        )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_details(order_id: int, service: OrderService = Depends(get_service)):
    """
    Get full details of a specific order, including items.
    """
    try:
        return service.get_order_details(order_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"API Error get_order_details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.post("/{order_id}/items", response_model=OrderResponse)
def add_item(
    order_id: int,
    item: OrderItemCreate,
    service: OrderService = Depends(get_service)
):
    """
    Add a dish to an existing order.
    Returns the updated order with new totals.
    """
    try:
        return service.add_item_to_order(order_id, item)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"API Error add_item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add item."
        )