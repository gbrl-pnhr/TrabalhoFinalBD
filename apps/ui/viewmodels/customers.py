from typing import List, Optional
import pandas as pd
from dataclasses import dataclass
from apps.api.modules import CustomerResponse, CustomerCreate
from apps.ui.services.customers import CustomerService
from apps.ui.utils.exceptions import AppError, ValidationError


@dataclass
class CustomerFormData:
    """DTO for form inputs to ensure type safety before hitting the logic layer."""

    name: str
    email: str
    phone: Optional[str] = None


class CustomersViewModel:
    """
    Business Logic for Customer Management.
    Handles data state, validation, and transformation.
    Zero Streamlit dependencies.
    """

    def __init__(self, customer_service: CustomerService):
        self._service = customer_service
        self.customers: List[CustomerResponse] = []
        self.last_error: Optional[str] = None

    def load_customers(self) -> None:
        """Fetches the customer directory from the backend."""
        self.last_error = None
        try:
            self.customers = self._service.get_customers()
        except AppError as e:
            self.last_error = str(e)
            self.customers = []

    def get_customers_dataframe(self) -> pd.DataFrame:
        """
        Transforms the domain models into a presentation-ready DataFrame.
        """
        if not self.customers:
            return pd.DataFrame(columns=["name", "email", "phone_number"])
        df = pd.DataFrame([c.model_dump() for c in self.customers])
        expected_cols = ["id", "name", "email", "phone_number"]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None

        return df

    def create_customer(self, form_data: CustomerFormData) -> bool:
        """
        Validates input and attempts to create a new customer.
        Returns True if successful, False otherwise (checks last_error).
        """
        self.last_error = None

        if not form_data.name.strip():
            self.last_error = "Name is required."
            return False

        if not form_data.email.strip() or "@" not in form_data.email:
            self.last_error = "A valid email address is required."
            return False

        try:
            payload = CustomerCreate(
                name=form_data.name, email=form_data.email, phone=form_data.phone
            )
            self._service.create_customer(payload)
            self.load_customers()
            return True
        except ValidationError as ve:
            self.last_error = f"Validation Failed: {ve}"
            return False
        except AppError as e:
            self.last_error = str(e)
            return False