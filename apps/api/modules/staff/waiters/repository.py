from typing import List
from pathlib import Path
import logging
from packages.common.src.models.waiters_models import WaiterCreate, WaiterResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"

class WaiterRepository:
    """Repository for accessing 'garcom' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def create_waiter(self, waiter: WaiterCreate) -> WaiterResponse:
        """Register a new waiter."""
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            logger.info(f"Creating waiter: {waiter.name}")
            try:
                cur.execute(
                    query,
                    {
                        "name": waiter.name,
                        "cpf": waiter.cpf,
                        "salary": waiter.salary,
                        "shift": waiter.shift,
                        "commission": waiter.commission,
                    },
                )
                row = cur.fetchone()
                self.conn.commit()

                if not row:
                    raise Exception("Failed to insert waiter")

                return WaiterResponse(
                    id=row["id_funcionario"],
                    name=row["nome"],
                    cpf=row["cpf"],
                    salary=row["salario"],
                    shift=row["turno"],
                    commission=row["comissao"],
                )
            except Exception as e:
                self.conn.rollback()
                logger.error(f"Error creating waiter: {e}")
                raise e

    def get_all_waiters(self) -> List[WaiterResponse]:
        """Fetch all waiters."""
        query = "SELECT id_funcionario, nome, cpf, salario, turno, comissao FROM garcom ORDER BY nome;"

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [
                WaiterResponse(
                    id=row["id_funcionario"],
                    name=row["nome"],
                    cpf=row["cpf"],
                    salary=row["salario"],
                    shift=row["turno"],
                    commission=row["comissao"],
                )
                for row in rows
            ]