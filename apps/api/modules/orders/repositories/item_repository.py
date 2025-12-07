from typing import List
from pathlib import Path
import logging
from packages.common.src.models.orders_models import OrderItemCreate, OrderItemResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent.parent / "queries" / "item"


class ItemRepository:
    """Repository for 'item_pedido' table operations."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def add_item(self, order_id: int, item: OrderItemCreate):
        """Inserts an item into the database."""
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(
                query,
                {
                    "order_id": order_id,
                    "dish_id": item.dish_id,
                    "quantity": item.quantity,
                    "notes": item.notes,
                },
            )
            self.conn.commit()

    def remove_item(self, item_id: int):
        """Removes an item from the database."""
        sql_file = QUERY_PATH / "delete.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query, {"item_id": item_id})
            self.conn.commit()

    def get_items_by_order(self, order_id: int) -> List[OrderItemResponse]:
        """Fetches all items for a specific order with Dish details."""
        sql_file = QUERY_PATH / "get_by_order.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query, {"order_id": order_id})
            rows = cur.fetchall()

            items = []
            for row in rows:
                qty = row["quantidade"]
                price = row["preco"]
                items.append(
                    OrderItemResponse(
                        id=row["id_item_pedido"],
                        dish_id=row["id_prato"],
                        quantity=qty,
                        notes=row["observacao"],
                        dish_name=row["nome_prato"],
                        unit_price=price,
                        total_price=price * qty,
                    )
                )
            return items