"""
frontend/schemas.py
Aggregates all backend models for use in the Frontend.
"""

from backend.modules import (
    WaiterResponse, WaiterCreate,
    ChefResponse, ChefCreate,
    DishResponse, DishCreate, DishUpdate,
    OrderResponse, OrderItemResponse, OrderCreate, OrderItemCreate,
    TableResponse, TableCreate,
    ReviewResponse, ReviewCreate, ReviewUpdate,
    CustomerResponse, CustomerCreate,
    DailyRevenue, DishPopularity, WaiterPerformance,
)