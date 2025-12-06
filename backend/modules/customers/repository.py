from typing import List
from pathlib import Path
import logging
from backend.modules.customers.models import CustomerCreate, CustomerResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"


class CustomerRepository:
    """Repository for accessing 'cliente' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def create_customer(self, customer: CustomerCreate) -> CustomerResponse:
        """
        Register a new customer in the database.

        Args:
            customer (CustomerCreate): The customer data.

        Returns:
            CustomerResponse: The created customer with ID.

        Raises:
            Exception: If database insertion fails (e.g., duplicate email).
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
                )
            except Exception as e:
                self.conn.rollback()
                logger.error(f"Error creating customer: {e}")
                raise e

    def get_all_customers(self) -> List[CustomerResponse]:
        """
        Fetch all registered customers.

        Returns:
            List[CustomerResponse]: List of all customers.
        """
        query = "SELECT id_cliente, nome, telefone, email FROM cliente ORDER BY nome;"

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [
                CustomerResponse(
                    id=row["id_cliente"],
                    name=row["nome"],
                    phone=row["telefone"],
                    email=row["email"],
                )
                for row in rows
            ]