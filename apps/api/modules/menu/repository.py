from typing import List, Optional
from pathlib import Path
import logging
import json

from packages.common.src.models.menu_models import DishCreate, DishResponse, DishUpdate
from packages.common.src.models.reviews_models import ReviewResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"


class MenuRepository:
    """Repository for accessing 'prato' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def delete_dish(self, dish_id: int) -> bool:
        """
        Deletes a dish from the database.
        Returns True if a row was deleted, False otherwise.
        """
        sql_file = QUERY_PATH / "delete.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query, {"id": dish_id})
            rows_deleted = cur.rowcount
            self.conn.commit()
            return rows_deleted > 0

    def get_categories(self) -> List[str]:
        """Fetch all unique categories currently in the database."""
        sql_file = QUERY_PATH / "categories.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [row["categoria"] for row in rows]

    def create_dish(self, dish: DishCreate) -> DishResponse:
        """
        Insert a new dish into the database.
        """
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            logger.info(f"Creating dish: {dish.nome}")
            cur.execute(
                query,
                {"name": dish.nome, "price": dish.preco, "category": dish.categoria},
            )
            row = cur.fetchone()
            self.conn.commit()
            if not row:
                raise Exception("Failed to insert dish")
            return DishResponse(
                id=row["id_prato"],
                nome=row["nome"],
                preco=row["preco"],
                categoria=row["categoria"],
                avaliacoes=[],
            )

    def get_all_dishes(self) -> List[DishResponse]:
        """
        Fetch all dishes populated with their reviews.
        """
        sql_file = QUERY_PATH / "list_populated.sql"
        query = sql_file.read_text()
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            results = []
            for row in rows:
                reviews_data = row["reviews"]
                if isinstance(reviews_data, str):
                    reviews_data = json.loads(reviews_data)
                reviews_list = [ReviewResponse(**r) for r in reviews_data]
                results.append(
                    DishResponse(
                        id=row["id_prato"],
                        nome=row["nome"],
                        preco=row["preco"],
                        categoria=row["categoria"],
                        avaliacoes=reviews_list,
                    )
                )
            return results

    def update_dish(self, dish_id: int, dish: DishUpdate) -> Optional[DishResponse]:
        """
        Update a dish's details.
        """
        sql_file = QUERY_PATH / "update.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(
                query,
                {
                    "name": dish.nome,
                    "price": dish.preco,
                    "category": dish.categoria,
                    "id": dish_id,
                },
            )
            row = cur.fetchone()
            self.conn.commit()

            if not row:
                return None

            return DishResponse(
                id=row["id_prato"],
                nome=row["nome"],
                preco=row["preco"],
                categoria=row["categoria"],
                avaliacoes=[],
            )