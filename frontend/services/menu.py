from typing import List
from services.api_client import APIClient
from schemas import DishResponse, DishCreate

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
        """
        Add a new dish to the menu.
        """
        response_data = self.client.post("/menu/dishes", dish.model_dump())
        return DishResponse.model_validate(response_data)