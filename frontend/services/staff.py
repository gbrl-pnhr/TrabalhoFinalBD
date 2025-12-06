from typing import List, Dict, Any
from services.api_client import APIClient

class StaffService:
    """
    Service layer for managing employees (Waiters and Chefs).
    """

    def __init__(self):
        self.client = APIClient()

    def get_waiters(self) -> List[Dict[str, Any]]:
        """
        List all registered waiters.

        Returns:
            List[Dict]: List of waiters.
        """
        return self.client.get("/staff/waiters")

    def create_waiter(self, waiter_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new waiter.

        Args:
            waiter_data (Dict): {name, cpf, hire_date}

        Returns:
            Dict: Created waiter object.
        """
        return self.client.post("/staff/waiters", waiter_data)

    def get_chefs(self) -> List[Dict[str, Any]]:
        """
        List all registered chefs.

        Returns:
            List[Dict]: List of chefs.
        """
        return self.client.get("/staff/chefs")

    def create_chef(self, chef_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new chef.

        Args:
            chef_data (Dict): {name, cpf, hire_date, specialty}

        Returns:
            Dict: Created chef object.
        """
        return self.client.post("/staff/chefs", chef_data)