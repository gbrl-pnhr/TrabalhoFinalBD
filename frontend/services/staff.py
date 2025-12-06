from typing import List
from services.api_client import APIClient
from frontend.schemas import WaiterResponse, WaiterCreate, ChefResponse, ChefCreate

class StaffService:
    """
    Service layer for managing employees (Waiters and Chefs).
    """

    def __init__(self):
        self.client = APIClient()

    def get_waiters(self) -> List[WaiterResponse]:
        """List all registered waiters."""
        data = self.client.get("/staff/waiters")
        return [WaiterResponse.model_validate(item) for item in data]

    def create_waiter(self, waiter_data: WaiterCreate) -> WaiterResponse:
        """Register a new waiter."""
        response = self.client.post("/staff/waiters", waiter_data.model_dump())
        return WaiterResponse.model_validate(response)

    def get_chefs(self) -> List[ChefResponse]:
        """List all registered chefs."""
        data = self.client.get("/staff/chefs")
        return [ChefResponse.model_validate(item) for item in data]

    def create_chef(self, chef_data: ChefCreate) -> ChefResponse:
        """Register a new chef."""
        response = self.client.post("/staff/chefs", chef_data.model_dump())
        return ChefResponse.model_validate(response)