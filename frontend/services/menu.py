from typing import List, Dict, Any
from services.api_client import APIClient

class MenuService:
    """
    Service layer for managing the restaurant menu.
    """

    def __init__(self):
        self.client = APIClient()

    def get_dishes(self) -> List[Dict[str, Any]]:
        """
        Get all dishes available in the menu.

        Returns:
            List[Dict]: List of dish objects.
        """
        return self.client.get("/menu/dishes")

    def create_dish(self, dish_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new dish to the menu.

        Args:
            dish_data (Dict): payload containing name, description, price, category.

        Returns:
            Dict: The created dish object.
        """
        return self.client.post("/menu/dishes", dish_data)