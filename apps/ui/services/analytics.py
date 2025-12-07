from typing import List
import sys
from pathlib import Path
import streamlit as st

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from apps.api.modules import DailyRevenue, DishPopularity, WaiterPerformance
from apps.ui.services.api_client import APIClient


class AnalyticsService:
    """
    Service layer for fetching business analytics.
    Implements Streamlit Caching to prevent redundant API calls.
    """

    def __init__(self):
        self.client = APIClient()

    @st.cache_data(ttl=60, show_spinner=False)
    def get_revenue_stats(_self) -> List[DailyRevenue]:
        """
        Fetch daily revenue statistics.
        Cached for 60 seconds.
        Note: '_self' argument prevents Streamlit from trying to hash the Service instance.
        """
        data = _self.client.get("/analytics/revenue")
        return [DailyRevenue.model_validate(item) for item in data]

    @st.cache_data(ttl=60, show_spinner=False)
    def get_popular_dishes(_self) -> List[DishPopularity]:
        """
        Fetch the top 10 most popular dishes.
        Cached for 60 seconds.
        """
        data = _self.client.get("/analytics/popular-dishes")
        return [DishPopularity.model_validate(item) for item in data]

    @st.cache_data(ttl=60, show_spinner=False)
    def get_staff_performance(_self) -> List[WaiterPerformance]:
        """
        Fetch performance stats for waiters.
        Cached for 60 seconds.
        """
        data = _self.client.get("/analytics/staff-performance")
        return [WaiterPerformance.model_validate(item) for item in data]