from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ReviewBase(BaseModel):
    """Base fields for a Review."""

    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = Field(
        None, max_length=500, description="Optional text comment"
    )


class ReviewCreate(ReviewBase):
    """Schema for submitting a new review."""

    customer_id: int = Field(..., description="ID of the customer")
    dish_id: int = Field(..., description="ID of the dish being reviewed")
    order_id: int = Field(..., description="ID of the order context")


class ReviewResponse(ReviewBase):
    """Schema for review response."""

    id: int = Field(..., description="Unique identifier of the review")
    created_at: datetime = Field(..., description="Timestamp of the review")
    customer_name: str = Field(..., description="Name of the customer (joined)")
    dish_name: str = Field(..., description="Name of the dish (joined)")

    model_config = ConfigDict(from_attributes=True)