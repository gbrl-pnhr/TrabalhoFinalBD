import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from typing import List
from apps.api.modules import CustomerResponse, CustomerCreate
from apps.ui.services.api_client import APIClient

class CustomerService:
    def __init__(self):
        self.client = APIClient()

    @st.cache_data(ttl=60, show_spinner=False)
    def get_customers(self) -> List[CustomerResponse]:
        data = self.client.get("/customers/")
        return [CustomerResponse.model_validate(c) for c in data]

    def create_customer(self, customer: CustomerCreate) -> CustomerResponse:
        data = self.client.post("/customers/", customer.model_dump())
        self.get_customers.clear()
        return CustomerResponse.model_validate(data)