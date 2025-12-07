from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

OrderStatus = Literal['ABERTO', 'FECHADO', 'CANCELADO']


class OrderItemBase(BaseModel):
    """Base fields for an order item."""

    id_prato: int = Field(..., description="ID of the dish (prato)")
    quantidade: int = Field(..., gt=0, description="Quantity of the dish")
    observacoes: Optional[str] = Field(None, description="Special instructions")


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int = Field(..., description="Unique identifier of the order item")
    nome_prato: str = Field(..., description="Name of the dish (joined data)")
    preco_unitario: Decimal = Field(..., description="Price of the dish at time of order")
    preco_total: Decimal = Field(..., description="Calculated total (price * quantity)")
    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    id_cliente: int = Field(..., description="ID of the paying customer")
    id_mesa: int = Field(..., description="ID of the table")
    id_garcom: int = Field(..., description="ID of the waiter")
    quantidade_cliente: int = Field(1, gt=0, description="Number of people at the table")


class OrderResponse(BaseModel):
    """Schema for Order Header details."""
    id: int = Field(..., description="Unique identifier of the order")
    id_cliente: int = Field(..., description="ID of the customer")
    criado_em: datetime = Field(..., description="Timestamp of creation")
    valor_total: Decimal = Field(..., description="Total accumulated value")
    status: OrderStatus = Field(..., description="Current status of the order")
    quantidade_cliente: int = Field(..., description="Number of people")
    nome_cliente: str = Field(..., description="Name of the customer")
    id_mesa: int = Field(..., description="Database ID of the table")
    id_garcom: int = Field(..., description="Database ID of the waiter")
    numero_mesa: int = Field(..., description="Physical Table number")
    nome_garcom: str = Field(..., description="Name of the waiter")
    itens: List[OrderItemResponse] = Field(
        default=[], description="List of items in the order"
    )
    model_config = ConfigDict(from_attributes=True)