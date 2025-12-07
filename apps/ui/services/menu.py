import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from typing import List
from apps.api.modules import DishResponse, DishCreate, DishUpdate
from apps.ui.services.api_client import APIClient

class MenuService:
    """
    Service layer for managing the restaurant menu.
    Cached because menus change rarely but are read often.
    """

    def __init__(self):
        self.client = APIClient()

    @st.cache_data(ttl=60, show_spinner=False)
    def get_dishes(self) -> List[DishResponse]:
        data = self.client.get("/menu/dishes")
        return [DishResponse.model_validate(item) for item in data]

    @st.cache_data(ttl=60, show_spinner=False)
    def get_categories(self) -> List[str]:
        return self.client.get("/menu/categories")

    def create_dish(self, dish: DishCreate) -> DishResponse:
        response_data = self.client.post("/menu/dishes", dish.model_dump(mode='json'))
        self.get_dishes.clear()
        self.get_categories.clear()
        return DishResponse.model_validate(response_data)

    def update_dish(self, dish_id: int, updates: DishUpdate) -> DishResponse:
        response_data = self.client.patch(
            f"/menu/dishes/{dish_id}",
            updates.model_dump(mode='json', exclude_unset=True)
        )
        self.get_dishes.clear()
        self.get_categories.clear()
        return DishResponse.model_validate(response_data)

    def delete_dish(self, dish_id: int) -> None:
        self.client.delete(f"/menu/dishes/{dish_id}")
        self.get_dishes.clear()
        self.get_categories.clear()