import logging
from decimal import Decimal
from typing import List
from fastapi import HTTPException
from backend.modules.orders.models import OrderCreate, OrderResponse, OrderItemCreate
from backend.modules.orders.repositories.order_repository import OrderRepository
from backend.modules.orders.repositories.item_repository import ItemRepository
from backend.modules.menu.repository import MenuRepository

logger = logging.getLogger(__name__)


class OrderService:
    """
    Business logic for Orders.
    Coordinates between OrderRepo, ItemRepo, and MenuRepo.
    """

    def __init__(self, db_connection):
        self.conn = db_connection
        self.order_repo = OrderRepository(db_connection)
        self.item_repo = ItemRepository(db_connection)
        self.menu_repo = MenuRepository(db_connection)

    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """Opens a new order and returns the details."""
        try:
            new_id = self.order_repo.create_order(order_data)
            return self.get_order_details(new_id)
        except Exception as e:
            logger.error(f"Service Error create_order: {e}")
            raise e

    def get_order_details(self, order_id: int) -> OrderResponse:
        """Fetches order header and appends items."""
        order = self.order_repo.get_order_details(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        items = self.item_repo.get_items_by_order(order_id)
        order.items = items
        calc_total = sum(i.total_price for i in items)
        if abs(calc_total - order.total_value) > Decimal("0.01"):
            logger.warning(
                f"Order {order_id} total mismatch. DB: {order.total_value}, Calc: {calc_total}"
            )

        return order

    def list_orders(self) -> List[OrderResponse]:
        """Lists all orders. For efficiency, does not load items for the list view."""
        return self.order_repo.list_active_orders()

    def add_item_to_order(
        self, order_id: int, item_data: OrderItemCreate
    ) -> OrderResponse:
        """
        Adds an item, calculates costs, and updates order total.
        Transactional logic.
        """
        try:
            dishes = self.menu_repo.get_all_dishes()
            target_dish = next((d for d in dishes if d.id == item_data.dish_id), None)
            if not target_dish:
                raise HTTPException(status_code=404, detail="Dish not found")
            self.item_repo.add_item(order_id, item_data)
            items = self.item_repo.get_items_by_order(order_id)
            new_total = sum(i.total_price for i in items)
            self.order_repo.update_order_total(order_id, new_total)
            return self.get_order_details(order_id)

        except Exception as e:
            logger.error(f"Service Error add_item_to_order: {e}")
            self.conn.rollback()
            raise e