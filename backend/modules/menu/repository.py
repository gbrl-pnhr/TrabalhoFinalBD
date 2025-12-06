from typing import List, Optional
from pathlib import Path
import logging

from backend.core.database import get_db_connection
from backend.modules.menu.models import DishCreate, DishResponse
logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"


class MenuRepository:
    """Repository for accessing 'prato' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def create_dish(self, dish: DishCreate) -> DishResponse:
        """
        Insert a new dish into the database.

        Args:
            dish (DishCreate): The dish data.

        Returns:
            DishResponse: The created dish with ID.
        """
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            logger.info(f"Creating dish: {dish.name}")
            cur.execute(
                query,
                {"name": dish.name, "price": dish.price, "category": dish.category},
            )
            row = cur.fetchone()
            self.conn.commit()
            if not row:
                raise Exception("Failed to insert dish")
            return DishResponse(
                id=row["id_prato"],
                name=row["nome"],
                price=row["preco"],
                category=row["categoria"],
            )

    def get_all_dishes(self) -> List[DishResponse]:
        """
        Fetch all dishes.

        Returns:
            List[DishResponse]: List of all dishes in the menu.
        """
        query = "SELECT id_prato, nome, preco, categoria FROM prato ORDER BY nome;"

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [
                DishResponse(
                    id=row["id_prato"],
                    name=row["nome"],
                    price=row["preco"],
                    category=row["categoria"],
                )
                for row in rows
            ]