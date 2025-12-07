from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, List
from packages.common.src.models.reviews_models import ReviewResponse


class DishBase(BaseModel):
    """Base fields for a Dish."""

    nome: str = Field(..., min_length=1, max_length=100, description="Name of the dish")
    preco: Decimal = Field(..., gt=0, decimal_places=2, description="Price of the dish")
    categoria: str = Field(
        ..., min_length=1, max_length=50, description="Category (e.g., Starter, Main)"
    )


class DishCreate(DishBase):
    """Schema for creating a new dish."""

    pass


class DishUpdate(BaseModel):
    """Schema for updating an existing dish."""

    nome: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Name of the dish"
    )
    preco: Optional[Decimal] = Field(
        None, gt=0, decimal_places=2, description="Price of the dish"
    )
    categoria: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Category (e.g., Starter, Main)"
    )


class DishResponse(DishBase):
    """Schema for dish response, including ID and nested Reviews."""

    id: int = Field(..., description="Unique identifier of the dish")
    avaliacoes: List[ReviewResponse] = Field(
        default=[], description="List of reviews for this dish"
    )

    model_config = ConfigDict(from_attributes=True)