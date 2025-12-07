import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path as PathParam, Request
from packages.common.src.models.orders_models import OrderCreate, OrderResponse, OrderItemCreate
from apps.api.modules.orders.service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])
logger = logging.getLogger(__name__)

async def get_db_connection(request: Request):
    async with request.app.state.pool.connection() as conn:
        yield conn

def get_service(conn=Depends(get_db_connection)):
    """Dependency injection for OrderService."""
    try:
        return OrderService(conn)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"API Error get_service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize order service.",
        )

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate, service: OrderService = Depends(get_service)
):
    """
    Open a new order (Table Check-in).
    Checks table capacity vs customer count.
    """
    try:
        return await service.create_order(order_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"API Error create_order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order.",
        )

@router.get("/", response_model=List[OrderResponse])
async def list_orders(service: OrderService = Depends(get_service)):
    """
    List all active orders.
    """
    try:
        return await service.list_orders()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"API Error list_orders: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_details(
    order_id: int = PathParam(..., description="ID of the order"),
    service: OrderService = Depends(get_service)
):
    """
    Get full details of a specific order, including items.
    """
    try:
        return await service.get_order_details(order_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"API Error get_order_details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

@router.post("/{order_id}/items", response_model=OrderResponse)
async def add_item(
    order_id: int,
    item: OrderItemCreate,
    service: OrderService = Depends(get_service)
):
    """
    Add a dish to an existing order (Must be open).
    Returns the updated order with new totals.
    """
    try:
        return await service.add_item_to_order(order_id, item)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"API Error add_item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

@router.delete("/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(
    order_id: int,
    item_id: int,
    service: OrderService = Depends(get_service)
):
    """Remove an item from an order (Must be OPEN)."""
    try:
        await service.remove_item_from_order(order_id, item_id)
        return None
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"API Error remove_item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

@router.patch("/{order_id}/close", response_model=OrderResponse)
async def close_order(
    order_id: int,
    service: OrderService = Depends(get_service)
):
    """Close/Finalize an order."""
    try:
        return await service.close_order(order_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"API Error close_order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )