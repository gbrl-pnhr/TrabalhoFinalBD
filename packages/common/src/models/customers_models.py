from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from packages.common.src.models.orders_models import OrderResponse


class CustomerBase(BaseModel):
    """Base fields for a Customer."""

    nome: str = Field(
        ..., min_length=1, max_length=100, description="Full name of the customer"
    )
    telefone: Optional[str] = Field(
        None, max_length=20, description="Contact phone number"
    )
    email: EmailStr = Field(..., max_length=100, description="Email address")


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer."""

    pass


class CustomerResponse(CustomerBase):
    """Schema for customer response, including DB ID and nested Orders."""

    id: int = Field(..., description="Unique identifier of the customer")
    pedidos: List[OrderResponse] = Field(
        default=[], description="List of all orders placed by this customer"
    )
    model_config = ConfigDict(from_attributes=True)