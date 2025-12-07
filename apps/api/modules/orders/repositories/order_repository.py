from typing import List, Optional
from pathlib import Path
import logging
import json
from decimal import Decimal

from packages.common.src.models.orders_models import OrderCreate, OrderResponse, OrderItemResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent.parent / "queries" / "order"


class OrderRepository:
    """Repository for 'pedido' table operations."""

    def __init__(self, db_connection):
        self.conn = db_connection

    async def create_order(self, order: OrderCreate) -> int:
        """Creates a new order header and returns its ID."""
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        async with self.conn.cursor() as cur:
            logger.info(
                f"Opening order for Customer {order.id_cliente} at Table {order.id_mesa}"
            )
            await cur.execute(
                query,
                {
                    "customer_id": order.id_cliente,
                    "table_id": order.id_mesa,
                    "waiter_id": order.id_garcom,
                    "people_count": order.quantidade_cliente,
                },
            )
            row = await cur.fetchone()
            await self.conn.commit()
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
            id_cliente=row["id_cliente"],
            criado_em=row["data_pedido"],
            valor_total=row["valor_total"],
            status=row["status"],
            quantidade_cliente=row["quantidade_pessoas"],
            nome_cliente=row["cliente_nome"],
            id_mesa=row["id_mesa"],
            id_garcom=row["id_garcom"],
            numero_mesa=row["mesa_numero"],
            nome_garcom=row["garcom_nome"],
            itens=items_list,
        )

    async def get_order_details(self, order_id: int) -> Optional[OrderResponse]:
        sql_file = QUERY_PATH / "get_details.sql"
        query = sql_file.read_text()

        async with self.conn.cursor() as cur:
            await cur.execute(query, {"order_id": order_id})
            row = await cur.fetchone()
            if not row:
                return None
            return self._map_row_to_response(row)

    async def list_active_orders(self) -> List[OrderResponse]:
        sql_file = QUERY_PATH / "list_active.sql"
        query = sql_file.read_text()

        async with self.conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            return [self._map_row_to_response(row) for row in rows]

    async def update_order_total(self, order_id: int, new_total: Decimal):
        sql_file = QUERY_PATH / "update_total.sql"
        query = sql_file.read_text()
        async with self.conn.cursor() as cur:
            await cur.execute(query, {"total": new_total, "id": order_id})
            await self.conn.commit()

    async def update_status(self, order_id: int, status: str):
        sql_file = QUERY_PATH / "update_status.sql"
        query = sql_file.read_text()
        async with self.conn.cursor() as cur:
            await cur.execute(query, {"status": status, "id": order_id})
            await self.conn.commit()