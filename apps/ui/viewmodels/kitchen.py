from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from apps.ui.services.order import OrderService
from apps.ui.utils.exceptions import AppError


@dataclass
class KitchenTicketItem:
    quantity: int
    dish_name: str
    notes: Optional[str]


@dataclass
class KitchenTicket:
    """
    Presentation-ready data for a Kitchen Ticket.
    Decouples the UI from the raw API response structure.
    """
    order_id: int
    table_label: str
    waiter_label: str
    time_elapsed_label: str
    items: List[KitchenTicketItem]
    is_alert: bool


class KitchenViewModel:
    """
    Business Logic for the Kitchen Display System.
    Handles data fetching, filtering, and transformation into UI-ready tickets.
    """

    def __init__(self, order_service: OrderService):
        self._service = order_service
        self.tickets: List[KitchenTicket] = []
        self.last_updated: str = ""
        self.last_error: Optional[str] = None

    def load_orders(self) -> None:
        """
        Fetches orders, filters for active kitchen tickets, and formats them.
        """
        self.last_error = None
        try:
            orders = self._service.list_orders()
            # Filter: Open orders that have items
            active_orders = [
                o for o in orders
                if str(o.status).lower() not in ["closed", "paid", "completed"]
                and o.items
            ]
            self.tickets = [self._to_ticket(o) for o in active_orders]
            self.last_updated = datetime.now().strftime("%H:%M:%S")
        except AppError as e:
            self.last_error = str(e)
            self.tickets = []

    def _to_ticket(self, order) -> KitchenTicket:
        """Transforms a raw Order model into a KitchenTicket DTO."""
        # 1. Calculate Time Label
        time_label = "Just Now"
        is_alert = False
        if hasattr(order, "created_at") and order.created_at:
            try:
                if isinstance(order.created_at, datetime):
                    created_dt = order.created_at
                else:
                    created_dt = datetime.fromisoformat(str(order.created_at))

                delta = datetime.now() - created_dt
                minutes = int(delta.total_seconds() / 60)
                time_label = f"{minutes} min ago"
                if minutes > 20:
                    is_alert = True
            except Exception:
                pass

        # 2. Format Table & Waiter
        # Fallback logic handles cases where table/waiter might be objects or flat IDs depending on API version
        table_disp = getattr(order, "table_number", getattr(order, "table_id", "?"))
        waiter_disp = getattr(order, "waiter_name", getattr(order, "waiter_id", "?"))

        # 3. Map Items
        items = [
            KitchenTicketItem(
                quantity=i.quantity,
                dish_name=i.dish_name,
                notes=i.notes
            )
            for i in order.items
        ]

        return KitchenTicket(
            order_id=order.id,
            table_label=str(table_disp),
            waiter_label=str(waiter_disp),
            time_elapsed_label=time_label,
            items=items,
            is_alert=is_alert
        )