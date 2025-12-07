from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ReviewBase(BaseModel):
    """Base fields for a Review."""

    nota: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comentario: Optional[str] = Field(
        None, max_length=500, description="Optional text comment"
    )


class ReviewCreate(ReviewBase):
    """Schema for submitting a new review."""

    id_cliente: int = Field(..., description="ID of the customer")
    id_prato: int = Field(..., description="ID of the dish being reviewed")
    id_pedido: int = Field(..., description="ID of the order context")


class ReviewUpdate(BaseModel):
    """Schema for updating an existing review."""

    nota: Optional[int] = Field(
        None, ge=1, le=5, description="New rating from 1 to 5"
    )
    comentario: Optional[str] = Field(None, max_length=500, description="New text comment")


class ReviewResponse(ReviewBase):
    """Schema for review response."""

    id: int = Field(..., description="Unique identifier of the review")
    criado_em: datetime = Field(..., description="Timestamp of the review")
    nome_cliente: str = Field(..., description="Name of the customer (joined)")
    nome_prato: str = Field(..., description="Name of the dish (joined)")

    model_config = ConfigDict(from_attributes=True)