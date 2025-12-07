import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from typing import List
from apps.api.modules import DishResponse, DishCreate, DishUpdate
from apps.ui.services.api_client import APIClient

class MenuService:
    """
    Service layer for managing the restaurant menu.
    """

    def __init__(self):
        self.client = APIClient()

    def get_dishes(self) -> List[DishResponse]:
        data = self.client.get("/menu/dishes")
        return [DishResponse.model_validate(item) for item in data]

    def get_categories(self) -> List[str]:
        """Fetch list of existing categories from the API."""
        return self.client.get("/menu/categories")

    def create_dish(self, dish: DishCreate) -> DishResponse:
        response_data = self.client.post("/menu/dishes", dish.model_dump(mode='json'))
        return DishResponse.model_validate(response_data)

    def update_dish(self, dish_id: int, updates: DishUpdate) -> DishResponse:
        """
        Update a single dish using the DishUpdate schema.
        """
        response_data = self.client.patch(
            f"/menu/dishes/{dish_id}",
            updates.model_dump(mode='json', exclude_unset=True)
        )
        return DishResponse.model_validate(response_data)

    def delete_dish(self, dish_id: int) -> None:
        """Remove a dish from the menu."""
        self.client.delete(f"/menu/dishes/{dish_id}")