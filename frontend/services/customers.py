from typing import List, Dict, Any
from services.api_client import APIClient

class CustomerService:
    """
    Service layer for managing customers.
    """

    def __init__(self):
        self.client = APIClient()

    def get_customers(self) -> List[Dict[str, Any]]:
        """
        Get all registered customers.

        Returns:
            List[Dict]: List of customers.
        """
        return self.client.get("/customers/")

    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new customer.

        Args:
            customer_data (Dict): {name, email, phone}

        Returns:
            Dict: Created customer object.
        """
        return self.client.post("/customers/", customer_data)