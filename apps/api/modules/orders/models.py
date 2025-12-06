from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

OrderStatus = Literal["OPEN", "CLOSED", "CANCELLED"]


class OrderItemBase(BaseModel):
    """Base fields for an order item."""

    dish_id: int = Field(..., description="ID of the dish (prato)")
    quantity: int = Field(..., gt=0, description="Quantity of the dish")
    notes: Optional[str] = Field(None, description="Special instructions")


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int = Field(..., description="Unique identifier of the order item")
    dish_name: str = Field(..., description="Name of the dish (joined data)")
    unit_price: Decimal = Field(..., description="Price of the dish at time of order")
    total_price: Decimal = Field(..., description="Calculated total (price * quantity)")
    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    customer_id: int = Field(..., description="ID of the paying customer")
    table_id: int = Field(..., description="ID of the table")
    waiter_id: int = Field(..., description="ID of the waiter")
    customer_count: int = Field(1, gt=0, description="Number of people at the table")


class OrderResponse(BaseModel):
    """Schema for Order Header details."""

    id: int = Field(..., description="Unique identifier of the order")
    created_at: datetime = Field(..., description="Timestamp of creation")
    total_value: Decimal = Field(..., description="Total accumulated value")
    status: OrderStatus = Field(..., description="Current status of the order")
    customer_count: int = Field(..., description="Number of people")
    customer_name: str = Field(..., description="Name of the customer")
    table_id: int = Field(..., description="Database ID of the table")
    waiter_id: int = Field(..., description="Database ID of the waiter")
    table_number: int = Field(..., description="Physical Table number")
    waiter_name: str = Field(..., description="Name of the waiter")
    items: List[OrderItemResponse] = Field(
        default=[], description="List of items in the order"
    )
    model_config = ConfigDict(from_attributes=True)