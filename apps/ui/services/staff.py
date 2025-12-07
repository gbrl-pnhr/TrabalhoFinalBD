import sys
import json
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from typing import List
from apps.api.modules import WaiterResponse, WaiterCreate, ChefResponse, ChefCreate
from apps.ui.services.api_client import APIClient

class StaffService:
    """
    Service layer for managing employees.
    Cached for dropdown performance.
    """

    def __init__(self):
        self.client = APIClient()

    @st.cache_data(ttl=60, show_spinner=False)
    def get_waiters(self) -> List[WaiterResponse]:
        data = self.client.get("/staff/waiters")
        return [WaiterResponse.model_validate(item) for item in data]

    def create_waiter(self, waiter_data: WaiterCreate) -> WaiterResponse:
        payload = json.loads(waiter_data.model_dump_json())
        response = self.client.post("/staff/waiters", payload)
        self.get_waiters.clear()
        return WaiterResponse.model_validate(response)

    def delete_waiter(self, waiter_id: int) -> None:
        self.client.delete(f"/staff/waiters/{waiter_id}")
        self.get_waiters.clear()

    @st.cache_data(ttl=60, show_spinner=False)
    def get_chefs(self) -> List[ChefResponse]:
        data = self.client.get("/staff/chefs")
        return [ChefResponse.model_validate(item) for item in data]

    def create_chef(self, chef_data: ChefCreate) -> ChefResponse:
        payload = json.loads(chef_data.model_dump_json())
        response = self.client.post("/staff/chefs", payload)
        self.get_chefs.clear()
        return ChefResponse.model_validate(response)

    def delete_chef(self, chef_id: int) -> None:
        self.client.delete(f"/staff/chefs/{chef_id}")
        self.get_chefs.clear()