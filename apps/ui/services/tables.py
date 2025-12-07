import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from typing import List
from apps.api.modules import TableResponse, TableCreate
from apps.ui.services.api_client import APIClient

class TableService:
    def __init__(self):
        self.client = APIClient()

    @st.cache_data(ttl=300, show_spinner=False)
    def get_tables(_self) -> List[TableResponse]:
        """Fetch all tables. Cached for 5 minutes."""
        data = _self.client.get("/tables/")
        return [TableResponse.model_validate(t) for t in data]

    def create_table(self, table: TableCreate) -> TableResponse:
        data = self.client.post("/tables/", table.model_dump())
        self.get_tables.clear()
        return TableResponse.model_validate(data)

    def delete_table(self, table_id: int) -> None:
        self.client.delete(f"/tables/{table_id}")
        self.get_tables.clear()