from typing import List, Dict, Any, Optional
from frontend.services.api_client import APIClient

class AnalyticsService:
    """
    Service layer for fetching analytics data from the backend.
    """

    @staticmethod
    def get_revenue_stats() -> List[Dict[str, Any]]:
        """
        Fetch daily revenue statistics.
        Returns: List of dictionaries (e.g., [{'date': '2023-10-01', 'total_revenue': 100.0}, ...])
        """
        data = APIClient.get("/analytics/revenue")
        return data if data else []

    @staticmethod
    def get_popular_dishes() -> List[Dict[str, Any]]:
        """
        Fetch top 10 popular dishes.
        """
        data = APIClient.get("/analytics/popular-dishes")
        return data if data else []

    @staticmethod
    def get_waiter_performance() -> List[Dict[str, Any]]:
        """
        Fetch performance stats for waiters.
        """
        data = APIClient.get("/analytics/staff-performance")
        return data if data else []