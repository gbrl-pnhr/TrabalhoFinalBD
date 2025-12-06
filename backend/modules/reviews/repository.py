from typing import List
from pathlib import Path
import logging
from backend.modules.reviews.models import ReviewCreate, ReviewResponse

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"


class ReviewRepository:
    """Repository for accessing 'avaliacao' table data."""

    def __init__(self, db_connection):
        self.conn = db_connection

    def create_review(self, review: ReviewCreate) -> ReviewResponse:
        """
        Submits a new review.
        Requires that the customer, dish, and order exist.
        """
        sql_file = QUERY_PATH / "create.sql"
        query = sql_file.read_text()
        # We need to fetch names for the response, so we might need a separate lookup
        # or a RETURNING combined with a JOIN (complex in pure SQL insert).
        # For simplicity, we insert, then fetch the names or pass them if known.
        # Here we will do a quick lookup after insert to ensure response model is full.

        with self.conn.cursor() as cur:
            logger.info(f"Creating review for Dish {review.dish_id}")
            try:
                cur.execute(
                    query,
                    {
                        "rating": review.rating,
                        "comment": review.comment,
                        "customer_id": review.customer_id,
                        "dish_id": review.dish_id,
                        "order_id": review.order_id,
                    },
                )
                row = cur.fetchone()
                self.conn.commit()
                if not row:
                    raise Exception("Failed to insert review")
                cur.execute(
                    "SELECT nome FROM cliente WHERE id_cliente = %s",
                    (review.customer_id,),
                )
                c_name = cur.fetchone()["nome"]
                cur.execute(
                    "SELECT nome FROM prato WHERE id_prato = %s", (review.dish_id,)
                )
                d_name = cur.fetchone()["nome"]
                return ReviewResponse(
                    id=row["id_avaliacao"],
                    rating=row["nota"],
                    comment=row["comentario"],
                    created_at=row["data_avaliacao"],
                    customer_name=c_name,
                    dish_name=d_name,
                )

            except Exception as e:
                self.conn.rollback()
                logger.error(f"Error creating review: {e}")
                raise e

    def get_reviews_by_dish(self, dish_id: int) -> List[ReviewResponse]:
        """Fetch all reviews for a specific dish."""
        sql_file = QUERY_PATH / "list_by_dish.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query, {"dish_id": dish_id})
            rows = cur.fetchall()

            return [
                ReviewResponse(
                    id=row["id_avaliacao"],
                    rating=row["nota"],
                    comment=row["comentario"],
                    created_at=row["data_avaliacao"],
                    customer_name=row["nome_cliente"],
                    dish_name=row["nome_prato"],
                )
                for row in rows
            ]