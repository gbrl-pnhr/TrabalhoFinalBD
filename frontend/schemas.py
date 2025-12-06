"""
frontend/schemas.py
Aggregates all backend models for use in the Frontend.
"""

from backend.modules import (
    WaiterResponse, WaiterCreate,
    ChefResponse, ChefCreate,
    DishResponse, DishCreate,
    OrderResponse, OrderItemResponse, OrderCreate,
    TableResponse,
    CustomerResponse,
    DailyRevenue, DishPopularity, WaiterPerformance
)