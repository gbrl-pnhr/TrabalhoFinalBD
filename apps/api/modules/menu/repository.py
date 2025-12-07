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
                reviews=[],
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
                        name=row["nome"],
                        price=row["preco"],
                        category=row["categoria"],
                        reviews=reviews_list,
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
                    "name": dish.name,
                    "price": dish.price,
                    "category": dish.category,
                    "id": dish_id,
                },
            )
            row = cur.fetchone()
            self.conn.commit()

            if not row:
                return None

            return DishResponse(
                id=row["id_prato"],
                name=row["nome"],
                price=row["preco"],
                category=row["categoria"],
                reviews=[],
            )