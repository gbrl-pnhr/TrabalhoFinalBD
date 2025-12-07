import sys
from pathlib import Path
import streamlit as st

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from apps.ui.services.reviews import ReviewService
from apps.ui.services.menu import MenuService
from apps.ui.services.customers import CustomerService
from apps.ui.viewmodels.reviews import ReviewsViewModel


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
    def get_reviews_viewmodel() -> ReviewsViewModel:
        """
        Factory method for ReviewsViewModel.
        Injects the required singletons.
        """
        return ReviewsViewModel(
            review_service=DIContainer._get_review_service(),
            menu_service=DIContainer._get_menu_service(),
            customer_service=DIContainer._get_customer_service(),
        )