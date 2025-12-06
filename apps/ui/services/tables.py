from typing import List
from apps.ui.services.api_client import APIClient
from apps.ui.schemas import TableResponse, TableCreate

class TableService:
    def __init__(self):
        self.client = APIClient()

    def get_tables(self) -> List[TableResponse]:
        data = self.client.get("/tables/")
        return [TableResponse.model_validate(t) for t in data]

    def create_table(self, table: TableCreate) -> TableResponse:
        data = self.client.post("/tables/", table.model_dump())
        return TableResponse.model_validate(data)