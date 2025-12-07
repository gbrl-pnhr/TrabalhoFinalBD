from typing import List
from pathlib import Path
import logging
from packages.common.src.models.analytics_models import (
    DailyRevenue,
    DishPopularity,
    WaiterPerformance,
)

logger = logging.getLogger(__name__)
QUERY_PATH = Path(__file__).parent / "queries"


class AnalyticsRepository:
    """
    Repository for Analytical Read-Only operations.
    Aggregates data for dashboards.
    """

    def __init__(self, db_connection):
        self.conn = db_connection

    def get_daily_revenue(self) -> List[DailyRevenue]:
        """
        Fetches revenue aggregated by day for the last 30 days.

        Returns:
            List[DailyRevenue]: List of daily stats.
        """
        sql_file = QUERY_PATH / "get_daily_revenue.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [
                DailyRevenue(
                    data=row["data"],
                    quantidade_ordem=row["total_pedidos"],
                    receita_total=row["receita_total"] or 0,
                )
                for row in rows
            ]

    def get_top_dishes(self) -> List[DishPopularity]:
        """
        Fetches top 10 selling dishes.

        Returns:
            List[DishPopularity]: List of dish stats.
        """
        sql_file = QUERY_PATH / "get_top_dishes.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [
                DishPopularity(
                    nome_prato=row["nome_prato"],
                    categoria=row["categoria"],
                    quantidade_vendida=row["total_vendido"],
                    receita_estimada=row["receita_estimada"] or 0,
                )
                for row in rows
            ]

    def get_waiter_performance(self) -> List[WaiterPerformance]:
        """
        Fetches sales performance per waiter.

        Returns:
            List[WaiterPerformance]: List of waiter stats.
        """
        sql_file = QUERY_PATH / "get_waiter_performance.sql"
        query = sql_file.read_text()

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [
                WaiterPerformance(
                    nome_garcom=row["nome_garcom"],
                    pedidos_atentidos=row["total_pedidos"],
                    vendas_totais=row["total_vendas"],
                )
                for row in rows
            ]