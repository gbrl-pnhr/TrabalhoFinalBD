from typing import List, Dict, Any
from frontend.services.api_client import APIClient

class TableService:
    """
    Service layer for managing restaurant tables.
    """

    def __init__(self):
        self.client = APIClient()

    def get_tables(self) -> List[Dict[str, Any]]:
        """
        Get all registered tables.

        Returns:
            List[Dict]: List of tables.
        """
        return self.client.get("/tables/")

    def create_table(self, table_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new table.

        Args:
            table_data (Dict): {number, capacity, location}

        Returns:
            Dict: Created table object.
        """
        return self.client.post("/tables/", table_data)