from typing import List, Dict, Any
from frontend.services.api_client import APIClient

class AnalyticsService:
    """
    Service layer for fetching business analytics.
    """

    def __init__(self):
        self.client = APIClient()

    def get_revenue_stats(self) -> List[Dict[str, Any]]:
        """
        Fetch daily revenue statistics for the last 30 days.

        Returns:
            List[Dict]: A list of daily revenue records.
        """
        return self.client.get("/analytics/revenue")

    def get_popular_dishes(self) -> List[Dict[str, Any]]:
        """
        Fetch the top 10 most popular dishes.

        Returns:
            List[Dict]: A list of dish popularity records.
        """
        return self.client.get("/analytics/popular-dishes")

    def get_staff_performance(self) -> List[Dict[str, Any]]:
        """
        Fetch performance stats for waiters.

        Returns:
            List[Dict]: A list of waiter performance records.
        """
        return self.client.get("/analytics/staff-performance")