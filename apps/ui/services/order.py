from typing import List
from apps.ui.services.api_client import APIClient
from apps.ui.schemas import OrderResponse, OrderCreate, OrderItemCreate

class OrderService:
    """
    Service layer for handling orders.
    """

    def __init__(self):
        self.client = APIClient()

    def create_order(self, order: OrderCreate) -> OrderResponse:
        """
        Open a new order (Table Check-in).
        """
        response = self.client.post("/orders/", order.model_dump())
        return OrderResponse.model_validate(response)

    def list_orders(self) -> List[OrderResponse]:
        data = self.client.get("/orders/")
        return [OrderResponse.model_validate(item) for item in data]

    def get_order_details(self, order_id: int) -> OrderResponse:
        data = self.client.get(f"/orders/{order_id}")
        return OrderResponse.model_validate(data)

    def add_item(self, order_id: int, item: OrderItemCreate) -> OrderResponse:
        """
        Add a dish to an existing order.
        """
        data = self.client.post(f"/orders/{order_id}/items", item.model_dump())
        return OrderResponse.model_validate(data)

    def remove_item(self, order_id: int, item_id: int) -> None:
        self.client.delete(f"/orders/{order_id}/items/{item_id}")

    def close_order(self, order_id: int) -> OrderResponse:
        data = self.client.patch(f"/orders/{order_id}/close")
        return OrderResponse.model_validate(data)