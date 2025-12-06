"""
Central export module for all Pydantic models used in the application.
Allows for streamlined imports in the Frontend.
"""

from backend.modules.analytics.models import (
    DailyRevenue,
    DishPopularity,
    WaiterPerformance,
)
from backend.modules.customers.models import (
    CustomerCreate,
    CustomerResponse,
)
from backend.modules.menu.models import (
    DishCreate,
    DishResponse,
    DishUpdate,
)
from backend.modules.orders.models import (
    OrderCreate,
    OrderResponse,
    OrderItemCreate,
    OrderItemResponse,
)
from backend.modules.reviews.models import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
)
from backend.modules.staff.chefs.models import (
    ChefCreate,
    ChefResponse,
)
from backend.modules.staff.waiters.models import (
    WaiterCreate,
    WaiterResponse,
)
from backend.modules.tables.models import (
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