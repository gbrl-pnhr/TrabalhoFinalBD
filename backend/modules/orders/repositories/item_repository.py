from typing import List
from pathlib import Path
import logging
from backend.modules.orders.models import OrderItemCreate, OrderItemResponse

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

    def get_items_by_order(self, order_id: int) -> List[OrderItemResponse]:
        """Fetches all items for a specific order with Dish details."""
        query = """
                SELECT
                    ip.id_item_pedido, ip.quantidade, ip.observacao,
                    pr.id_prato, pr.nome as nome_prato, pr.preco
                FROM item_pedido ip
                         JOIN prato pr ON ip.id_prato = pr.id_prato
                WHERE ip.id_pedido = %(order_id)s; \
                """
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