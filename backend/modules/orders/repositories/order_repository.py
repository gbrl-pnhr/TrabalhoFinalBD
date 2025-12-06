from typing import List, Optional
from pathlib import Path
import logging
from decimal import Decimal

from backend.modules.orders.models import OrderCreate, OrderResponse, OrderItemResponse

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
                },
            )
            row = cur.fetchone()
            self.conn.commit()
            if not row:
                raise Exception("Failed to create order")
            return row["id_pedido"]

    def get_order_details(self, order_id: int) -> Optional[OrderResponse]:
        """Fetches order header + joins with customer/table/staff."""
        query = """
                SELECT
                    p.id_pedido, p.data_pedido, p.valor_total,
                    c.nome as cliente_nome,
                    m.numero as mesa_numero,
                    g.nome as garcom_nome
                FROM pedido p
                         JOIN cliente c ON p.id_cliente = c.id_cliente
                         JOIN mesa m ON p.id_mesa = m.id_mesa
                         JOIN garcom g ON p.id_funcionario = g.id_funcionario
                WHERE p.id_pedido = %(order_id)s; \
                """

        with self.conn.cursor() as cur:
            cur.execute(query, {"order_id": order_id})
            row = cur.fetchone()
            if not row:
                return None

            return OrderResponse(
                id=row["id_pedido"],
                created_at=row["data_pedido"],
                total_value=row["valor_total"],
                customer_name=row["cliente_nome"],
                table_number=row["mesa_numero"],
                waiter_name=row["garcom_nome"],
                items=[],
            )

    def list_active_orders(self) -> List[OrderResponse]:
        """Lists all orders (simplified view without items)."""
        query = """
                SELECT
                    p.id_pedido, p.data_pedido, p.valor_total,
                    c.nome as cliente_nome,
                    m.numero as mesa_numero,
                    g.nome as garcom_nome
                FROM pedido p
                         JOIN cliente c ON p.id_cliente = c.id_cliente
                         JOIN mesa m ON p.id_mesa = m.id_mesa
                         JOIN garcom g ON p.id_funcionario = g.id_funcionario
                ORDER BY p.data_pedido DESC; \
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [
                OrderResponse(
                    id=row["id_pedido"],
                    created_at=row["data_pedido"],
                    total_value=row["valor_total"],
                    customer_name=row["cliente_nome"],
                    table_number=row["mesa_numero"],
                    waiter_name=row["garcom_nome"],
                    items=[],
                )
                for row in rows
            ]

    def update_order_total(self, order_id: int, new_total: Decimal):
        """Updates the total value of an order."""
        query = "UPDATE pedido SET valor_total = %(total)s WHERE id_pedido = %(id)s;"
        with self.conn.cursor() as cur:
            cur.execute(query, {"total": new_total, "id": order_id})
            self.conn.commit()