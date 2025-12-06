"""
Central export module for all Pydantic models used in the application.
Allows for streamlined imports in the Frontend.
"""

from apps.api.modules.analytics.models import (
    DailyRevenue,
    DishPopularity,
    WaiterPerformance,
)
from apps.api.modules.customers.models import (
    CustomerCreate,
    CustomerResponse,
)
from apps.api.modules.menu.models import (
    DishCreate,
    DishResponse,
    DishUpdate,
)
from apps.api.modules.orders.models import (
    OrderCreate,
    OrderResponse,
    OrderItemCreate,
    OrderItemResponse,
)
from apps.api.modules.reviews.models import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
)
from apps.api.modules.staff.chefs.models import (
    ChefCreate,
    ChefResponse,
)
from apps.api.modules.staff.waiters.models import (
    WaiterCreate,
    WaiterResponse,
)
from apps.api.modules.tables.models import (
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