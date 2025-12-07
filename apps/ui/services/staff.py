import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from typing import List
from apps.api.modules import WaiterResponse, WaiterCreate, ChefResponse, ChefCreate
from apps.ui.services.api_client import APIClient

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

    def delete_waiter(self, waiter_id: int) -> None:
        """Fire a waiter."""
        self.client.delete(f"/staff/waiters/{waiter_id}")

    def get_chefs(self) -> List[ChefResponse]:
        """List all registered chefs."""
        data = self.client.get("/staff/chefs")
        return [ChefResponse.model_validate(item) for item in data]

    def create_chef(self, chef_data: ChefCreate) -> ChefResponse:
        """Register a new chef."""
        response = self.client.post("/staff/chefs", chef_data.model_dump())
        return ChefResponse.model_validate(response)

    def delete_chef(self, chef_id: int) -> None:
        """Fire a chef."""
        self.client.delete(f"/staff/chefs/{chef_id}")