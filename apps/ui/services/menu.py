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

    def create_dish(self, dish: DishCreate) -> DishResponse:
        response_data = self.client.post("/menu/dishes", dish.model_dump())
        return DishResponse.model_validate(response_data)

    def update_dish(self, dish_id: int, updates: DishUpdate) -> DishResponse:
        """
        Update a single dish using the DishUpdate schema.
        """
        response_data = self.client.patch(
            f"/menu/dishes/{dish_id}",
            updates.model_dump(exclude_unset=True)
        )
        return DishResponse.model_validate(response_data)

    def delete_dish(self, dish_id: int) -> None:
        """Remove a dish from the menu."""
        self.client.delete(f"/menu/dishes/{dish_id}")