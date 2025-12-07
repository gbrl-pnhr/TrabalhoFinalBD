import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from typing import List
from apps.api.modules import TableResponse, TableCreate
from apps.ui.services.api_client import APIClient

class TableService:
    def __init__(self):
        self.client = APIClient()

    def get_tables(self) -> List[TableResponse]:
        """Fetch all tables."""
        data = self.client.get("/tables/")
        return [TableResponse.model_validate(t) for t in data]

    def create_table(self, table: TableCreate) -> TableResponse:
        """Register a new table."""
        data = self.client.post("/tables/", table.model_dump())
        return TableResponse.model_validate(data)

    def delete_table(self, table_id: int) -> None:
        """Remove a table from the layout."""
        self.client.delete(f"/tables/{table_id}")