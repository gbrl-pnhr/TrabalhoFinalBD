from typing import List, Optional
from pathlib import Path
import logging

from packages.common.src.models.tables_models import TableCreate, TableResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"


class TableRepository:
    """Repository for accessing 'mesa' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    async def delete_table(self, table_id: int) -> bool:
        sql_file = QUERY_PATH / "delete.sql"
        query = sql_file.read_text()
        async with self.conn.cursor() as cur:
            await cur.execute(query, {"id": table_id})
            deleted = cur.rowcount
            await self.conn.commit()
            return deleted > 0

    async def create_table(self, table: TableCreate) -> TableResponse:
        """
        Register a new table in the database.
        """
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        async with self.conn.cursor() as cur:
            logger.info(f"Creating table #{table.numero} at {table.localizacao}")
            try:
                await cur.execute(
                    query,
                    {
                        "number": table.numero,
                        "capacity": table.capacidade,
                        "location": table.localizacao,
                    },
                )
                row = await cur.fetchone()
                await self.conn.commit()

                if not row:
                    raise Exception("Failed to insert table")

                return TableResponse(
                    id=row["id_mesa"],
                    numero=row["numero"],
                    capacidade=row["capacidade"],
                    localizacao=row["localizacao"],
                    eh_ocupada=False
                )
            except Exception as e:
                await self.conn.rollback()
                logger.error(f"Error creating table: {e}")
                raise e

    async def get_all_tables(self) -> List[TableResponse]:
        """
        Fetch all tables with occupancy status.
        """
        sql_file = QUERY_PATH / "list.sql"
        query = sql_file.read_text()

        async with self.conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()

            return [
                TableResponse(
                    id=row["id_mesa"],
                    numero=row["numero"],
                    capacidade=row["capacidade"],
                    localizacao=row["localizacao"],
                    eh_ocupada=row["is_occupied"]
                )
                for row in rows
            ]

    async def get_table_by_id(self, table_id: int) -> Optional[TableResponse]:
        """Fetch a specific table by ID."""
        sql_file = QUERY_PATH / "get_by_id.sql"
        query = sql_file.read_text()

        async with self.conn.cursor() as cur:
            await cur.execute(query, {"id": table_id})
            row = await cur.fetchone()

            if not row:
                return None

            return TableResponse(
                id=row["id_mesa"],
                numero=row["numero"],
                capacidade=row["capacidade"],
                localizacao=row["localizacao"],
                eh_ocupada=row["is_occupied"]
            )