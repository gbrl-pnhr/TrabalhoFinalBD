from typing import List, Optional, Set
from concurrent.futures import ThreadPoolExecutor
from apps.api.modules import WaiterResponse, WaiterCreate, ChefResponse, ChefCreate
from apps.ui.services.staff import StaffService
from apps.ui.utils.exceptions import AppError


class StaffViewModel:
    """
    Business Logic for the Staff Management Page.
    Handles parallel data fetching for Waiters and Chefs.
    """

    def __init__(self, staff_service: StaffService):
        self._service = staff_service
        self.waiters: List[WaiterResponse] = []
        self.chefs: List[ChefResponse] = []
        self.last_error: Optional[str] = None

    def load_staff(self) -> None:
        """
        Refreshes the local state of waiters and chefs using Parallel Execution.
        """
        self.last_error = None
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_waiters = executor.submit(self._service.get_waiters)
            future_chefs = executor.submit(self._service.get_chefs)
            try:
                self.waiters = future_waiters.result()
                self.chefs = future_chefs.result()
            except AppError as e:
                self.last_error = str(e)
                self.waiters = []
                self.chefs = []
            except Exception as e:
                self.last_error = f"Unexpected error: {str(e)}"
                self.waiters = []
                self.chefs = []

    def get_existing_specialties(self) -> List[str]:
        """Extracts unique specialties from existing chefs for autocomplete."""
        specialties: Set[str] = {c.especialidade for c in self.chefs if c.especialidade}
        return sorted(list(specialties))

    def get_existing_shifts(self) -> List[str]:
        """Extracts unique shifts from existing waiters for autocomplete."""
        shifts: Set[str] = {w.turno for w in self.waiters if w.turno}
        return sorted(list(shifts))

    def hire_waiter(
        self, name: str, cpf: str, salary: float, commission: float, shift: str
    ) -> bool:
        """
        Attempts to register a new waiter.
        Returns True if successful, False otherwise (check last_error).
        """
        self.last_error = None
        try:
            payload = WaiterCreate(
                nome=name, cpf=cpf, salario=salary, comissao=commission, turno=shift
            )
            self._service.create_waiter(payload)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False
        except ValueError as e:
            self.last_error = f"Validation Error: {e}"
            return False

    def fire_waiter(self, waiter_id: int) -> bool:
        """Terminates a waiter's employment."""
        self.last_error = None
        try:
            self._service.delete_waiter(waiter_id)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False

    def hire_chef(self, name: str, cpf: str, salary: float, specialty: str) -> bool:
        """
        Attempts to register a new chef.
        Returns True if successful.
        """
        self.last_error = None
        try:
            payload = ChefCreate(nome=name, cpf=cpf, salario=salary, especialidade=specialty)
            self._service.create_chef(payload)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False
        except ValueError as e:
            self.last_error = f"Validation Error: {e}"
            return False

    def fire_chef(self, chef_id: int) -> bool:
        """Terminates a chef's employment."""
        self.last_error = None
        try:
            self._service.delete_chef(chef_id)
            return True
        except AppError as e:
            self.last_error = str(e)
            return False