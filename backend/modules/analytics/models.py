from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class DailyRevenue(BaseModel):
    """Schema for daily revenue aggregation."""

    date: date = Field(..., description="Date of sales")
    total_revenue: Decimal = Field(..., description="Total revenue for that day")
    order_count: int = Field(..., description="Number of orders placed")
    model_config = ConfigDict(from_attributes=True)


class DishPopularity(BaseModel):
    """Schema for dish sales statistics."""

    dish_name: str = Field(..., description="Name of the dish")
    category: str = Field(..., description="Dish category")
    total_sold: int = Field(..., description="Total quantity sold")
    estimated_revenue: Decimal = Field(..., description="Estimated revenue generated")
    model_config = ConfigDict(from_attributes=True)


class WaiterPerformance(BaseModel):
    """Schema for waiter performance statistics."""

    waiter_name: str = Field(..., description="Name of the waiter")
    orders_handled: int = Field(..., description="Total orders managed")
    total_sales: Decimal = Field(..., description="Total sales value generated")
    model_config = ConfigDict(from_attributes=True)