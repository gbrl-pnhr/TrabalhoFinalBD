import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from typing import List
from apps.api.modules import OrderCreate, OrderResponse, OrderItemCreate
from apps.ui.services.api_client import APIClient

class OrderService:
    """
    Service layer for handling orders.
    """

    def __init__(self):
        self.client = APIClient()


    @st.cache_data(ttl=10, show_spinner=False)
    def list_orders(self) -> List[OrderResponse]:
        """
        Fetches all orders. Cached for 10 seconds.
        Note: '_self' is used to exclude the service instance from hashing if needed,
        though Streamlit handles Pydantic/Simple classes well.
        """
        data = self.client.get("/orders/")
        return [OrderResponse.model_validate(item) for item in data]

    @st.cache_data(ttl=10, show_spinner=False)
    def get_order_details(self, order_id: int) -> OrderResponse:
        """Fetches a single order. Cached for 10 seconds."""
        data = self.client.get(f"/orders/{order_id}")
        return OrderResponse.model_validate(data)


    def create_order(self, order: OrderCreate) -> OrderResponse:
        """Open a new order and invalidate list cache."""
        response = self.client.post("/orders/", order.model_dump())
        self.list_orders.clear()
        return OrderResponse.model_validate(response)

    def add_item(self, order_id: int, item: OrderItemCreate) -> OrderResponse:
        """Add item, invalidate specific order cache and list cache."""
        data = self.client.post(f"/orders/{order_id}/items", item.model_dump())
        self.get_order_details.clear()
        self.list_orders.clear()
        return OrderResponse.model_validate(data)

    def remove_item(self, order_id: int, item_id: int) -> None:
        self.client.delete(f"/orders/{order_id}/items/{item_id}")
        self.get_order_details.clear()
        self.list_orders.clear()

    def close_order(self, order_id: int) -> OrderResponse:
        data = self.client.patch(f"/orders/{order_id}/close")
        self.get_order_details.clear()
        self.list_orders.clear()
        return OrderResponse.model_validate(data)