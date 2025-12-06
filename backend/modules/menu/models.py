from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class DishBase(BaseModel):
    """Base fields for a Dish."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the dish")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Price of the dish")
    category: str = Field(..., min_length=1, max_length=50, description="Category (e.g., Starter, Main)")

class DishCreate(DishBase):
    """Schema for creating a new dish."""
    pass

class DishResponse(DishBase):
    """Schema for dish response, including ID."""
    id: int = Field(..., description="Unique identifier of the dish")
    model_config = ConfigDict(from_attributes=True)