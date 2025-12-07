from typing import List

from apps.api.modules import DailyRevenue, DishPopularity, WaiterPerformance
from apps.ui.services.api_client import APIClient

class AnalyticsService:
    """
    Service layer for fetching business analytics using strict typing.
    """

    def __init__(self):
        self.client = APIClient()

    def get_revenue_stats(self) -> List[DailyRevenue]:
        """
        Fetch daily revenue statistics.
        """
        data = self.client.get("/analytics/revenue")
        return [DailyRevenue.model_validate(item) for item in data]

    def get_popular_dishes(self) -> List[DishPopularity]:
        """
        Fetch the top 10 most popular dishes.
        """
        data = self.client.get("/analytics/popular-dishes")
        return [DishPopularity.model_validate(item) for item in data]

    def get_staff_performance(self) -> List[WaiterPerformance]:
        """
        Fetch performance stats for waiters.
        """
        data = self.client.get("/analytics/staff-performance")
        return [WaiterPerformance.model_validate(item) for item in data]