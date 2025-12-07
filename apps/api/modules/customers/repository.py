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

    def create_customer(self, customer: CustomerCreate) -> CustomerResponse:
        """
        Register a new customer in the database.
        """
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            logger.info(f"Creating customer: {customer.name}")
            try:
                cur.execute(
                    query,
                    {
                        "name": customer.name,
                        "phone": customer.phone,
                        "email": customer.email,
                    },
                )
                row = cur.fetchone()
                self.conn.commit()

                if not row:
                    raise Exception("Failed to insert customer")

                return CustomerResponse(
                    id=row["id_cliente"],
                    name=row["nome"],
                    phone=row["telefone"],
                    email=row["email"],
                    orders=[],  # New customer has no orders
                )
            except Exception as e:
                self.conn.rollback()
                logger.error(f"Error creating customer: {e}")
                raise e

    def get_all_customers(self) -> List[CustomerResponse]:
        """
        Fetch all registered customers with their full order history.
        """
        sql_file = QUERY_PATH / "list_populated.sql"
        query = sql_file.read_text()
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            results = []
            for row in rows:
                orders_data = row["orders"]
                if isinstance(orders_data, str):
                    orders_data = json.loads(orders_data)
                orders_list = [OrderResponse(**o) for o in orders_data]
                results.append(
                    CustomerResponse(
                        id=row["id_cliente"],
                        name=row["nome"],
                        phone=row["telefone"],
                        email=row["email"],
                        orders=orders_list,
                    )
                )
            return results