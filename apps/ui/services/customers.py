from typing import List
from apps.ui.services.api_client import APIClient
from apps.ui.schemas import CustomerResponse, CustomerCreate

class CustomerService:
    def __init__(self):
        self.client = APIClient()

    def get_customers(self) -> List[CustomerResponse]:
        data = self.client.get("/customers/")
        return [CustomerResponse.model_validate(c) for c in data]

    def create_customer(self, customer: CustomerCreate) -> CustomerResponse:
        data = self.client.post("/customers/", customer.model_dump())
        return CustomerResponse.model_validate(data)