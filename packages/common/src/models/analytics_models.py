from datetime import date as date_type
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class DailyRevenue(BaseModel):
    """Schema for daily revenue aggregation."""

    data: date_type = Field(..., description="Date of sales")
    receita_total: Decimal = Field(..., description="Total revenue for that day")
    quantidade_ordem: int = Field(..., description="Number of orders placed")
    model_config = ConfigDict(from_attributes=True)


class DishPopularity(BaseModel):
    """Schema for dish sales statistics."""

    nome_prato: str = Field(..., description="Name of the dish")
    categoria: str = Field(..., description="Dish category")
    quantidade_vendida: int = Field(..., description="Total quantity sold")
    receita_estimada: Decimal = Field(..., description="Estimated revenue generated")
    model_config = ConfigDict(from_attributes=True)


class WaiterPerformance(BaseModel):
    """Schema for waiter performance statistics."""

    nome_garcom: str = Field(..., description="Name of the waiter")
    pedidos_atentidos: int = Field(..., description="Total orders managed")
    vendas_totais: Decimal = Field(..., description="Total sales value generated")
    model_config = ConfigDict(from_attributes=True)