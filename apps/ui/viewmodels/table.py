from typing import List, Optional, Set
import pandas as pd
from apps.api.modules import TableResponse, TableCreate
from apps.ui.services.tables import TableService
from apps.ui.utils.exceptions import AppError


class TableViewModel:
    """
    Business Logic for Table Management.
    Handles data fetching, next-number calculation, and validation.
    Zero Streamlit dependencies.
    """

    def __init__(self, table_service: TableService):
        self._service = table_service
        self.tables: List[TableResponse] = []
        self.last_error: Optional[str] = None

    def load_tables(self) -> None:
        """Fetches latest table layout from backend."""
        self.last_error = None
        try:
            self.tables = self._service.get_tables()
            self.tables.sort(key=lambda t: t.number)
        except AppError as e:
            self.last_error = str(e)
            self.tables = []

    def get_tables_dataframe(self) -> pd.DataFrame:
        """Transforms table list into a DataFrame for display."""
        if not self.tables:
            return pd.DataFrame()
        return pd.DataFrame([t.model_dump() for t in self.tables])

    def get_existing_locations(self) -> List[str]:
        """Extracts unique locations for the dropdown."""
        locations: Set[str] = {t.location for t in self.tables if t.location}
        return sorted(list(locations))

    def get_next_suggestion(self) -> int:
        """Calculates the next available table number based on max current."""
        if not self.tables:
            return 1
        occupied_numbers = [t.number for t in self.tables]
        return max(occupied_numbers) + 1

    def is_number_occupied(self, number: int) -> bool:
        """Checks if a table number already exists."""
        return any(t.number == number for t in self.tables)

    def add_table(self, number: int, capacity: int, location: str) -> bool:
        """
        Validates and attempts to create a new table.
        """
        self.last_error = None

        if number < 1:
            self.last_error = "Table number must be positive."
            return False
        if capacity < 1:
            self.last_error = "Capacity must be at least 1."
            return False
        if not location.strip():
            self.last_error = "Location name is required."
            return False
        if self.is_number_occupied(number):
            self.last_error = f"Table {number} already exists."
            return False

        try:
            payload = TableCreate(number=number, capacity=capacity, location=location)
            self._service.create_table(payload)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False

    def delete_table(self, table_id: int) -> bool:
        """Attempts to delete a table."""
        self.last_error = None
        try:
            self._service.delete_table(table_id)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False