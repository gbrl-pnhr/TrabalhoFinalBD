from typing import List, Optional
from pathlib import Path
import logging
from packages.common.src.models.reviews_models import ReviewCreate, ReviewResponse, ReviewUpdate

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"


class ReviewRepository:
    """
    Repository for accessing 'avaliacao' table data.
    Enforces business logic regarding review eligibility.
    """

    def __init__(self, db_connection):
        self.conn = db_connection

    @staticmethod
    async def _check_eligibility(cur, customer_id: int, order_id: int, dish_id: int) -> bool:
        """
        Verifies if the customer actually ordered the dish in the specific order.
        """
        sql_file = QUERY_PATH / "check_eligibility.sql"
        query = sql_file.read_text()
        await cur.execute(
            query,
            {"customer_id": customer_id, "order_id": order_id, "dish_id": dish_id},
        )
        return await cur.fetchone() is not None

    async def create_review(self, review: ReviewCreate) -> ReviewResponse:
        """
        Submits a new review with strict eligibility checks.
        """
        sql_create = (QUERY_PATH / "create.sql").read_text()
        sql_details = (QUERY_PATH / "get_details.sql").read_text()
        async with self.conn.cursor() as cur:
            logger.info(
                f"Attempting to create review for Dish {review.id_prato} by Customer {review.id_cliente}"
            )
            if not await self._check_eligibility(
                cur, review.id_cliente, review.id_pedido, review.id_prato
            ):
                logger.warning(
                    f"Review rejected: Customer {review.id_cliente} did not order Dish {review.id_prato} in Order {review.id_pedido}"
                )
                raise ValueError(
                    "Eligibility Error: Customer did not order this dish in the specified order."
                )
            try:
                await cur.execute(
                    sql_create,
                    {
                        "rating": review.nota,
                        "comment": review.comentario,
                        "customer_id": review.id_cliente,
                        "dish_id": review.id_prato,
                        "order_id": review.id_pedido,
                    },
                )
                row_id = await cur.fetchone()
                if not row_id:
                    raise Exception("Failed to insert review (No ID returned).")
                new_id = row_id["id_avaliacao"]
                await cur.execute(sql_details, {"review_id": new_id})
                row = await cur.fetchone()
                await self.conn.commit()
                if not row:
                    raise Exception("Failed to fetch created review details.")
                return ReviewResponse(
                    id=row["id_avaliacao"],
                    nota=row["nota"],
                    comentario=row["comentario"],
                    criado_em=row["data_avaliacao"],
                    nome_cliente=row["nome_cliente"],
                    nome_prato=row["nome_prato"],
                )

            except Exception as e:
                await self.conn.rollback()
                if not isinstance(e, ValueError):
                    logger.exception(f"Database error creating review: {e}")
                raise e

    async def get_reviews_by_dish(self, dish_id: int) -> List[ReviewResponse]:
        """
        Fetch all reviews for a specific dish.
        """
        sql_file = QUERY_PATH / "list_by_dish.sql"
        query = sql_file.read_text()

        async with self.conn.cursor() as cur:
            await cur.execute(query, {"dish_id": dish_id})
            rows = await cur.fetchall()

            return [
                ReviewResponse(
                    id=row["id_avaliacao"],
                    nota=row["nota"],
                    comentario=row["comentario"],
                    criado_em=row["data_avaliacao"],
                    nome_cliente=row["nome_cliente"],
                    nome_prato=row["nome_prato"],
                )
                for row in rows
            ]

    async def delete_review(self, review_id: int) -> bool:
        sql_file = QUERY_PATH / "delete.sql"
        query = sql_file.read_text()
        async with self.conn.cursor() as cur:
            await cur.execute(query, {"id": review_id})
            deleted = cur.rowcount
            await self.conn.commit()
            return deleted > 0

    async def update_review(
        self, review_id: int, review_update: ReviewUpdate
    ) -> Optional[ReviewResponse]:
        """
        Updates an existing review's rating or comment.
        """
        sql_update = (QUERY_PATH / "update.sql").read_text()
        sql_details = (QUERY_PATH / "get_details.sql").read_text()

        async with self.conn.cursor() as cur:
            try:
                await cur.execute(
                    sql_update,
                    {
                        "rating": review_update.nota,
                        "comment": review_update.comentario,
                        "review_id": review_id,
                    },
                )
                row_id = await cur.fetchone()
                if not row_id:
                    await self.conn.rollback()
                    return None
                await cur.execute(sql_details, {"review_id": review_id})
                row = await cur.fetchone()
                await self.conn.commit()
                if not row:
                    return None
                return ReviewResponse(
                    id=row["id_avaliacao"],
                    nota=row["nota"],
                    comentario=row["comentario"],
                    criado_em=row["data_avaliacao"],
                    nome_cliente=row["nome_cliente"],
                    nome_prato=row["nome_prato"],
                )

            except Exception as e:
                await self.conn.rollback()
                logger.exception(f"Database error updating review {review_id}: {e}")
                raise e