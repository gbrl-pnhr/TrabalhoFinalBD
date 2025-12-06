from typing import List, Dict, Any
from frontend.services.api_client import APIClient

class OrderService:
    """
    Service layer for handling orders (Check-ins, adding items, closing).
    """

    def __init__(self):
        self.client = APIClient()

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Open a new order (Table Check-in).

        Args:
            order_data (Dict): {table_id, customer_count, waiter_id, customer_ids}

        Returns:
            Dict: The created order.
        """
        return self.client.post("/orders/", order_data)

    def list_orders(self) -> List[Dict[str, Any]]:
        """
        List all active/open orders.

        Returns:
            List[Dict]: List of order summaries.
        """
        return self.client.get("/orders/")

    def get_order_details(self, order_id: int) -> Dict[str, Any]:
        """
        Get full details of a specific order.

        Args:
            order_id (int): The ID of the order.

        Returns:
            Dict: Detailed order object including items.
        """
        return self.client.get(f"/orders/{order_id}")

    def add_item(self, order_id: int, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a dish to an existing order.

        Args:
            order_id (int): The ID of the order.
            item_data (Dict): {dish_id, quantity, notes}

        Returns:
            Dict: Updated order object.
        """
        return self.client.post(f"/orders/{order_id}/items", item_data)

    def remove_item(self, order_id: int, item_id: int) -> None:
        """
        Remove an item from an order.

        Args:
            order_id (int): The order ID.
            item_id (int): The specific item ID within the order.
        """
        return self.client.delete(f"/orders/{order_id}/items/{item_id}")

    def close_order(self, order_id: int) -> Dict[str, Any]:
        """
        Finalize/Close an order.

        Args:
            order_id (int): The order ID.

        Returns:
            Dict: The closed order object.
        """
        return self.client.patch(f"/orders/{order_id}/close")