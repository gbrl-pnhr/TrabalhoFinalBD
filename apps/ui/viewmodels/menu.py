from typing import List, Optional, Dict
import pandas as pd
from dataclasses import dataclass
from apps.api.modules import DishResponse, DishCreate, DishUpdate
from apps.ui.services.menu import MenuService
from apps.ui.utils.exceptions import AppError


@dataclass
class DishFormData:
    name: str
    price: float
    category: str


class MenuViewModel:
    """
    Business Logic for Menu Management.
    Handles data fetching, validation, and transformation for the View.
    """

    def __init__(self, menu_service: MenuService):
        self._service = menu_service
        self.dishes: List[DishResponse] = []
        self.categories: List[str] = []
        self.last_error: Optional[str] = None

    def load_data(self) -> None:
        """Fetches dishes and categories from the backend."""
        self.last_error = None
        try:
            self.dishes = self._service.get_dishes()
            self.categories = self._service.get_categories()
        except AppError as e:
            self.last_error = str(e)
            self.dishes = []
            self.categories = []

    def get_dishes_dataframe(self) -> pd.DataFrame:
        """Transforms dish list into a Pandas DataFrame for display."""
        if not self.dishes:
            return pd.DataFrame(columns=["name", "category", "price"])

        return pd.DataFrame([d.model_dump() for d in self.dishes])

    def get_dish_lookup(self) -> Dict[int, str]:
        """Returns a dictionary for selectboxes: {id: "Name ($Price)"}."""
        return {d.id: f"{d.name} (${d.price:.2f})" for d in self.dishes}

    def get_dish_by_id(self, dish_id: int) -> Optional[DishResponse]:
        """Finds a dish object by ID from the local cache."""
        return next((d for d in self.dishes if d.id == dish_id), None)

    def create_dish(self, data: DishFormData) -> bool:
        """Attempts to create a new dish."""
        self.last_error = None

        # Basic Validation
        if not data.name:
            self.last_error = "Dish name is required."
            return False
        if data.price <= 0:
            self.last_error = "Price must be greater than zero."
            return False
        if not data.category or data.category.startswith("➕"):
            self.last_error = "Invalid category selected."
            return False

        try:
            payload = DishCreate(
                name=data.name, price=data.price, category=data.category
            )
            self._service.create_dish(payload)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False
        except ValueError as e:
            self.last_error = f"Validation Error: {e}"
            return False

    def update_dish(self, dish_id: int, name: str, price: float) -> bool:
        """Attempts to update an existing dish."""
        self.last_error = None
        try:
            payload = DishUpdate(name=name, price=price)
            self._service.update_dish(dish_id, payload)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False

    def delete_dish(self, dish_id: int) -> bool:
        """Attempts to delete a dish."""
        self.last_error = None
        try:
            self._service.delete_dish(dish_id)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False