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

    async def delete_waiter(self, waiter_id: int) -> bool:
        sql_file = QUERY_PATH / "delete.sql"
        query = sql_file.read_text()
        async with self.conn.cursor() as cur:
            await cur.execute(query, {"id": waiter_id})
            deleted = cur.rowcount
            await self.conn.commit()
            return deleted > 0

    async def create_waiter(self, waiter: WaiterCreate) -> WaiterResponse:
        """Register a new waiter."""
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        async with self.conn.cursor() as cur:
            logger.info(f"Creating waiter: {waiter.nome}")
            try:
                await cur.execute(
                    query,
                    {
                        "name": waiter.nome,
                        "cpf": waiter.cpf,
                        "salary": waiter.salario,
                        "shift": waiter.turno,
                        "commission": waiter.comissao,
                    },
                )
                row = await cur.fetchone()
                await self.conn.commit()

                if not row:
                    raise Exception("Failed to insert waiter")

                return WaiterResponse(
                    id=row["id_funcionario"],
                    nome=row["nome"],
                    cpf=row["cpf"],
                    salario=row["salario"],
                    turno=row["turno"],
                    comissao=row["comissao"],
                )
            except Exception as e:
                await self.conn.rollback()
                logger.error(f"Error creating waiter: {e}")
                raise e

    async def get_all_waiters(self) -> List[WaiterResponse]:
        """Fetch all waiters."""
        query = "SELECT id_funcionario, nome, cpf, salario, turno, comissao FROM garcom ORDER BY nome;"

        async with self.conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()

            return [
                WaiterResponse(
                    id=row["id_funcionario"],
                    nome=row["nome"],
                    cpf=row["cpf"],
                    salario=row["salario"],
                    turno=row["turno"],
                    comissao=row["comissao"],
                )
                for row in rows
            ]