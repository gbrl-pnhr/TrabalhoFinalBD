from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class OrderItemBase(BaseModel):
    """Base fields for an order item."""

    dish_id: int = Field(..., description="ID of the dish (prato)")
    quantity: int = Field(..., gt=0, description="Quantity of the dish")
    notes: Optional[str] = Field(
        None, description="Special instructions (e.g., 'No onions')"
    )


class OrderItemCreate(OrderItemBase):
    """Schema for adding an item to an order."""

    pass


class OrderItemResponse(OrderItemBase):
    """Schema for item response."""

    id: int = Field(..., description="Unique identifier of the order item")
    dish_name: str = Field(..., description="Name of the dish (joined data)")
    unit_price: Decimal = Field(..., description="Price of the dish at time of order")
    total_price: Decimal = Field(..., description="Calculated total (price * quantity)")

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    """Schema for opening a new order/table."""

    customer_id: int = Field(..., description="ID of the customer")
    table_id: int = Field(..., description="ID of the table")
    waiter_id: int = Field(..., description="ID of the waiter")


class OrderResponse(BaseModel):
    """Schema for Order Header details."""

    id: int = Field(..., description="Unique identifier of the order")
    created_at: datetime = Field(..., description="Timestamp of creation")
    total_value: Decimal = Field(
        ..., description="Total accumulated value of the order"
    )
    customer_name: str = Field(..., description="Name of the customer")
    table_number: int = Field(..., description="Table number")
    waiter_name: str = Field(..., description="Name of the waiter")
    status: str = "Active"
    items: List[OrderItemResponse] = Field(
        default=[], description="List of items in the order"
    )
    model_config = ConfigDict(from_attributes=True)