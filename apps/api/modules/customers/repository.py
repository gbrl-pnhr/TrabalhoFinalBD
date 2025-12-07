from typing import List
from pathlib import Path
import logging
import json
from packages.common.src.models.customers_models import CustomerCreate, CustomerResponse
from packages.common.src.models.orders_models import OrderResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"


class CustomerRepository:
    """Repository for accessing 'cliente' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    async def create_customer(self, customer: CustomerCreate) -> CustomerResponse:
        """
        Register a new customer in the database.
        """
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        async with self.conn.cursor() as cur:
            logger.info(f"Creating customer: {customer.nome}")
            try:
                await cur.execute(
                    query,
                    {
                        "name": customer.nome,
                        "phone": customer.telefone,
                        "email": customer.email,
                    },
                )
                row = await cur.fetchone()
                await self.conn.commit()

                if not row:
                    raise Exception("Failed to insert customer")

                return CustomerResponse(
                    id=row["id_cliente"],
                    nome=row["nome"],
                    telefone=row["telefone"],
                    email=row["email"],
                    pedidos=[],
                )
            except Exception as e:
                await self.conn.rollback()
                logger.error(f"Error creating customer: {e}")
                raise e

    async def get_all_customers(self) -> List[CustomerResponse]:
        """
        Fetch all registered customers with their full order history.
        """
        sql_file = QUERY_PATH / "list_populated.sql"
        query = sql_file.read_text()
        async with self.conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
            results = []
            for row in rows:
                orders_data = row["pedidos"]
                if isinstance(orders_data, str):
                    orders_data = json.loads(orders_data)
                if orders_data is None:
                    orders_data = []
                orders_list = [OrderResponse(**o) for o in orders_data]
                results.append(
                    CustomerResponse(
                        id=row["id_cliente"],
                        nome=row["nome"],
                        telefone=row["telefone"],
                        email=row["email"],
                        pedidos=orders_list,
                    )
                )
            return results