import sys
from pathlib import Path
import streamlit as st

from apps.ui.viewmodels.customers import CustomersViewModel
from apps.ui.viewmodels.kitchen import KitchenViewModel
from apps.ui.viewmodels.menu import MenuViewModel

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))
from apps.ui.services.reviews import ReviewService
from apps.ui.services.menu import MenuService
from apps.ui.services.customers import CustomerService
from apps.ui.services.analytics import AnalyticsService
from apps.ui.services.order import OrderService
from apps.ui.services.tables import TableService
from apps.ui.services.staff import StaffService
from apps.ui.viewmodels.reviews import ReviewsViewModel
from apps.ui.viewmodels.dashboard import DashboardViewModel
from apps.ui.viewmodels.orders import OrdersViewModel
from apps.ui.viewmodels.staff import StaffViewModel
from apps.ui.viewmodels.table import TableViewModel


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
    def _get_analytics_service() -> AnalyticsService:
        return AnalyticsService()

    @staticmethod
    @st.cache_resource
    def _get_order_service() -> OrderService:
        return OrderService()

    @staticmethod
    @st.cache_resource
    def _get_table_service() -> TableService:
        return TableService()

    @staticmethod
    @st.cache_resource
    def _get_staff_service() -> StaffService:
        return StaffService()

    @staticmethod
    def get_reviews_viewmodel() -> ReviewsViewModel:
        return ReviewsViewModel(
            review_service=DIContainer._get_review_service(),
            menu_service=DIContainer._get_menu_service(),
            customer_service=DIContainer._get_customer_service(),
        )

    @staticmethod
    def get_dashboard_viewmodel() -> DashboardViewModel:
        return DashboardViewModel(
            analytics_service=DIContainer._get_analytics_service()
        )

    @staticmethod
    def get_orders_viewmodel() -> OrdersViewModel:
        """Factory for OrdersViewModel with all dependencies injected."""
        return OrdersViewModel(
            order_service=DIContainer._get_order_service(),
            customer_service=DIContainer._get_customer_service(),
            table_service=DIContainer._get_table_service(),
            staff_service=DIContainer._get_staff_service(),
        )

    @staticmethod
    def get_staff_viewmodel() -> StaffViewModel:
        return StaffViewModel(staff_service=DIContainer._get_staff_service())

    @staticmethod
    def get_table_viewmodel() -> TableViewModel:
        """Factory for TableViewModel."""
        return TableViewModel(table_service=DIContainer._get_table_service())

    @staticmethod
    def get_menu_viewmodel() -> MenuViewModel:
        """Factory for TableViewModel."""
        return MenuViewModel(menu_service=DIContainer._get_menu_service())

    @staticmethod
    def get_customers_viewmodel() -> CustomersViewModel:
        """Factory for CustomersViewModel with dependencies injected."""
        return CustomersViewModel(customer_service=DIContainer._get_customer_service())

    @staticmethod
    def get_kitchen_viewmodel() -> KitchenViewModel:
        """Factory for KitchenViewModel."""
        return KitchenViewModel(
            order_service=DIContainer._get_order_service()
        )