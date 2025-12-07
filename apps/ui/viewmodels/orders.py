from typing import List, Dict, Optional
from dataclasses import dataclass
from apps.api.modules import (
    OrderResponse,
    OrderCreate,
    OrderItemCreate,
)
from apps.ui.services.order import OrderService
from apps.ui.services.customers import CustomerService
from apps.ui.services.tables import TableService
from apps.ui.services.staff import StaffService
from apps.ui.utils.exceptions import AppError


@dataclass
class NewOrderOptions:
    """DTO to hold dropdown options for creating a new order."""

    customers: Dict[int, str]
    tables: Dict[int, str]
    waiters: Dict[int, str]


class OrdersViewModel:
    """
    Business Logic for the Orders Page.
    Handles data state and command execution.
    """

    def __init__(
        self,
        order_service: OrderService,
        customer_service: CustomerService,
        table_service: TableService,
        staff_service: StaffService,
    ):
        self._order_service = order_service
        self._customer_service = customer_service
        self._table_service = table_service
        self._staff_service = staff_service
        self.active_orders: List[OrderResponse] = []
        self.last_error: Optional[str] = None

    def load_active_orders(self) -> None:
        """Fetches orders that are not closed/paid."""
        self.last_error = None
        try:
            all_orders = self._order_service.list_orders()
            self.active_orders = [
                o
                for o in all_orders
                if str(o.status).lower() not in ["closed", "paid", "completed"]
            ]
            self.active_orders.sort(key=lambda x: x.id, reverse=True)
        except AppError as e:
            self.last_error = str(e)

    def get_order_by_id(self, order_id: int) -> Optional[OrderResponse]:
        """
        Fetches the latest state of a single order.
        Used by fragments to refresh specific cards without reloading the whole list.
        """
        try:
            return self._order_service.get_order_details(order_id)
        except AppError:
            return None

    def get_new_order_options(self) -> NewOrderOptions:
        """Fetches auxiliary data needed to open a new table."""
        try:
            customers = self._customer_service.get_customers()
            tables = self._table_service.get_tables()
            waiters = self._staff_service.get_waiters()
            cust_map = {c.id: c.name for c in customers}
            waiter_map = {w.id: w.name for w in waiters}
            table_map = {
                t.id: f"Table {t.number} ({t.capacity} Seats) - {t.location}"
                for t in tables
                if not t.is_occupied
            }
            return NewOrderOptions(
                customers=cust_map, tables=table_map, waiters=waiter_map
            )
        except AppError as e:
            self.last_error = f"Failed to load options: {e}"
            return NewOrderOptions({}, {}, {})

    def check_table_capacity(self, table_id: int, guest_count: int) -> Optional[str]:
        """Pre-validation check for table capacity."""
        try:
            tables = self._table_service.get_tables()
            selected = next((t for t in tables if t.id == table_id), None)
            if selected and guest_count > selected.capacity:
                return (
                    f"⚠️ Capacity Exceeded! Table {selected.number} holds {selected.capacity}, "
                    f"but you have {guest_count} guests."
                )
        except AppError:
            pass
        return None

    def create_order(
        self, customer_id: int, table_id: int, waiter_id: int, count: int
    ) -> bool:
        self.last_error = None
        try:
            payload = OrderCreate(
                customer_id=customer_id,
                table_id=table_id,
                waiter_id=waiter_id,
                customer_count=count,
            )
            self._order_service.create_order(payload)
            return True
        except (AppError, ValueError) as e:
            self.last_error = str(e)
            return False

    def add_item_to_order(self, order_id: int, dish_id: int, quantity: int) -> bool:
        self.last_error = None
        if quantity < 1:
            self.last_error = "Quantity must be at least 1."
            return False

        try:
            item = OrderItemCreate(dish_id=dish_id, quantity=quantity)
            self._order_service.add_item(order_id, item)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False

    def remove_item_from_order(self, order_id: int, item_id: int) -> bool:
        self.last_error = None
        try:
            self._order_service.remove_item(order_id, item_id)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False

    def close_order(self, order_id: int) -> bool:
        self.last_error = None
        try:
            self._order_service.close_order(order_id)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False