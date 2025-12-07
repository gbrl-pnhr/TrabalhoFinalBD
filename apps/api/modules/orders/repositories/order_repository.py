from typing import List, Optional
from pathlib import Path
import logging
import json
from decimal import Decimal

from apps.api.modules.orders.models import OrderCreate, OrderResponse, OrderItemResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent.parent / "queries" / "order"


class OrderRepository:
    """Repository for 'pedido' table operations."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def create_order(self, order: OrderCreate) -> int:
        """Creates a new order header and returns its ID."""
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            logger.info(
                f"Opening order for Customer {order.customer_id} at Table {order.table_id}"
            )
            cur.execute(
                query,
                {
                    "customer_id": order.customer_id,
                    "table_id": order.table_id,
                    "waiter_id": order.waiter_id,
                    "people_count": order.customer_count,
                },
            )
            row = cur.fetchone()
            self.conn.commit()
            if not row:
                raise Exception("Failed to create order")
            return row["id_pedido"]

    @staticmethod
    def _map_row_to_response(row) -> OrderResponse:
        """Helper to map a DB row to OrderResponse."""
        items_data = row.get(
            "items"
        )
        if isinstance(items_data, str):
            items_data = json.loads(items_data)
        if not items_data:
            items_list = []
        else:
            items_list = [OrderItemResponse(**item) for item in items_data]
        return OrderResponse(
            id=row["id_pedido"],
            customer_id=row["id_cliente"],
            created_at=row["data_pedido"],
            total_value=row["valor_total"],
            status=row["status"],
            customer_count=row["quantidade_pessoas"],
            customer_name=row["cliente_nome"],
            table_id=row["id_mesa"],
            waiter_id=row["id_garcom"],
            table_number=row["mesa_numero"],
            waiter_name=row["garcom_nome"],
            items=items_list,
        )

    def get_order_details(self, order_id: int) -> Optional[OrderResponse]:
        sql_file = QUERY_PATH / "get_details.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query, {"order_id": order_id})
            row = cur.fetchone()
            if not row:
                return None
            return self._map_row_to_response(row)

    def list_active_orders(self) -> List[OrderResponse]:
        sql_file = QUERY_PATH / "list_active.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [self._map_row_to_response(row) for row in rows]

    def update_order_total(self, order_id: int, new_total: Decimal):
        sql_file = QUERY_PATH / "update_total.sql"
        query = sql_file.read_text()
        with self.conn.cursor() as cur:
            cur.execute(query, {"total": new_total, "id": order_id})
            self.conn.commit()

    def update_status(self, order_id: int, status: str):
        sql_file = QUERY_PATH / "update_status.sql"
        query = sql_file.read_text()
        with self.conn.cursor() as cur:
            cur.execute(query, {"status": status, "id": order_id})
            self.conn.commit()