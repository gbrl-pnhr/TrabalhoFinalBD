import sys
from pathlib import Path
import streamlit as st

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from apps.ui.services.reviews import ReviewService
from apps.ui.services.menu import MenuService
from apps.ui.services.customers import CustomerService
from apps.ui.services.analytics import AnalyticsService  # Added
from apps.ui.viewmodels.reviews import ReviewsViewModel
from apps.ui.viewmodels.dashboard import DashboardViewModel  # Added


class DIContainer:
    """
    Dependency Injection Container.
    Manages the lifecycle of Services and ViewModels.
    """

    @staticmethod
    @st.cache_resource
    def _get_review_service() -> ReviewService:
        return ReviewService()

    @staticmethod
    @st.cache_resource
    def _get_menu_service() -> MenuService:
        return MenuService()

    @staticmethod
    @st.cache_resource
    def _get_customer_service() -> CustomerService:
        return CustomerService()

    @staticmethod
    @st.cache_resource
    def _get_analytics_service() -> AnalyticsService:  # Added
        return AnalyticsService()

    @staticmethod
    def get_reviews_viewmodel() -> ReviewsViewModel:
        return ReviewsViewModel(
            review_service=DIContainer._get_review_service(),
            menu_service=DIContainer._get_menu_service(),
            customer_service=DIContainer._get_customer_service(),
        )

    @staticmethod
    def get_dashboard_viewmodel() -> DashboardViewModel:  # Added
        """Factory for DashboardViewModel"""
        return DashboardViewModel(
            analytics_service=DIContainer._get_analytics_service()
        )