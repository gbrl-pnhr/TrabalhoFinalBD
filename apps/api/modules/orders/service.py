import logging
from decimal import Decimal
from typing import List
from fastapi import HTTPException, status
from packages.common.src.models.orders_models import OrderCreate, OrderResponse, OrderItemCreate
from apps.api.modules.orders.repositories.order_repository import OrderRepository
from apps.api.modules.orders.repositories.item_repository import ItemRepository
from apps.api.modules.menu.repository import MenuRepository
from apps.api.modules.tables.repository import TableRepository

logger = logging.getLogger(__name__)


class OrderService:
    """
    Business logic for Orders.
    Coordinates between OrderRepo, ItemRepo, MenuRepo, and TableRepo.
    """

    def __init__(self, db_connection):
        self.conn = db_connection
        self.order_repo = OrderRepository(db_connection)
        self.item_repo = ItemRepository(db_connection)
        self.menu_repo = MenuRepository(db_connection)
        self.table_repo = TableRepository(db_connection)

    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """
        Opens a new order.
        Validates that customer count does not exceed table capacity.
        """
        table = self.table_repo.get_table_by_id(order_data.id_mesa)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        if order_data.quantidade_cliente > table.capacidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Table capacity exceeded. Table fits {table.capacidade}, but request has {order_data.quantidade_cliente} people.",
            )
        try:
            new_id = self.order_repo.create_order(order_data)
            return self.get_order_details(new_id)
        except Exception as e:
            logger.error(f"Service Error create_order: {e}")
            raise e

    def get_order_details(self, order_id: int) -> OrderResponse:
        """
        Fetches order header and items.
        Refactored: Now relies on Repository deep fetch.
        """
        order = self.order_repo.get_order_details(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        calc_total = sum(i.preco_total for i in order.itens)
        if abs(calc_total - order.valor_total) > Decimal("0.01"):
            logger.warning(
                f"Order {order_id} total mismatch. DB: {order.valor_total}, Calc: {calc_total}"
            )

        return order

    def list_orders(self) -> List[OrderResponse]:
        """Lists all ACTIVE orders deeply populated."""
        return self.order_repo.list_active_orders()

    def add_item_to_order(
        self, order_id: int, item_data: OrderItemCreate
    ) -> OrderResponse:
        """
        Adds an item to an existing order.
        Validates order status is OPEN.
        """
        order = self.order_repo.get_order_details(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status != "OPEN":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot add items to a {order.status} order.",
            )
        try:
            dishes = self.menu_repo.get_all_dishes()
            target_dish = next((d for d in dishes if d.id == item_data.id_prato), None)
            if not target_dish:
                raise HTTPException(status_code=404, detail="Dish not found")
            self.item_repo.add_item(order_id, item_data)
            self._recalculate_total(order_id)
            return self.get_order_details(order_id)

        except Exception as e:
            logger.error(f"Service Error add_item_to_order: {e}")
            self.conn.rollback()
            raise e

    def remove_item_from_order(self, order_id: int, item_id: int):
        """Removes an item and recalculates total."""
        order = self.order_repo.get_order_details(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status != "OPEN":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove items from a closed order.",
            )

        try:
            self.item_repo.remove_item(item_id)
            self._recalculate_total(order_id)
        except Exception as e:
            logger.error(f"Error removing item: {e}")
            raise e

    def close_order(self, order_id: int):
        """Finalizes the order."""
        order = self.order_repo.get_order_details(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        self.order_repo.update_status(order_id, "CLOSED")
        return self.get_order_details(order_id)

    def _recalculate_total(self, order_id: int):
        """Helper to sum items and update order header."""
        items = self.item_repo.get_items_by_order(order_id)
        new_total = sum(i.preco_total for i in items)
        self.order_repo.update_order_total(order_id, new_total)