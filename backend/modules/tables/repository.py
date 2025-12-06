from typing import List
from pathlib import Path
import logging

from backend.modules.tables.models import TableCreate, TableResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"


class TableRepository:
    """Repository for accessing 'mesa' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def create_table(self, table: TableCreate) -> TableResponse:
        """
        Register a new table in the database.

        Args:
            table (TableCreate): The table data.

        Returns:
            TableResponse: The created table with ID.

        Raises:
            Exception: If database insertion fails (e.g., duplicate number).
        """
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            logger.info(f"Creating table #{table.number} at {table.location}")
            try:
                cur.execute(
                    query,
                    {
                        "number": table.number,
                        "capacity": table.capacity,
                        "location": table.location,
                    },
                )
                row = cur.fetchone()
                self.conn.commit()

                if not row:
                    raise Exception("Failed to insert table")

                return TableResponse(
                    id=row["id_mesa"],
                    number=row["numero"],
                    capacity=row["capacidade"],
                    location=row["localizacao"],
                )
            except Exception as e:
                self.conn.rollback()
                logger.error(f"Error creating table: {e}")
                raise e

    def get_all_tables(self) -> List[TableResponse]:
        """
        Fetch all tables.

        Returns:
            List[TableResponse]: List of all tables ordered by number.
        """
        query = "SELECT id_mesa, numero, capacidade, localizacao FROM mesa ORDER BY numero;"

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [
                TableResponse(
                    id=row["id_mesa"],
                    number=row["numero"],
                    capacity=row["capacidade"],
                    location=row["localizacao"],
                )
                for row in rows
            ]