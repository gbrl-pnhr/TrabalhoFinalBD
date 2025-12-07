"""
Central export module for all Pydantic models used in the application.
Allows for streamlined imports in the Frontend.
"""

from packages.common.src.models.analytics_models import (
    DailyRevenue,
    DishPopularity,
    WaiterPerformance,
)
from packages.common.src.models.customers_models import (
    CustomerCreate,
    CustomerResponse,
)
from packages.common.src.models.menu_models import (
    DishCreate,
    DishResponse,
    DishUpdate,
)
from packages.common.src.models.orders_models import (
    OrderCreate,
    OrderResponse,
    OrderItemCreate,
    OrderItemResponse,
)
from packages.common.src.models.reviews_models import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
)
from packages.common.src.models.chef_models import (
    ChefCreate,
    ChefResponse,
)
from packages.common.src.models.waiters_models import (
    WaiterCreate,
    WaiterResponse,
)
from packages.common.src.models.tables_models import (
    TableCreate,
    TableResponse,
)

__all__ = [
    "DailyRevenue",
    "DishPopularity",
    "WaiterPerformance",
    "CustomerCreate",
    "CustomerResponse",
    "OrderItemCreate",
    "DishCreate",
    "DishResponse",
    "DishUpdate",
    "OrderCreate",
    "OrderResponse",
    "OrderItemCreate",
    "OrderItemResponse",
    "ReviewCreate",
    "ReviewResponse",
    "ReviewUpdate",
    "ChefCreate",
    "ChefResponse",
    "WaiterCreate",
    "WaiterResponse",
    "TableCreate",
    "TableResponse",
]