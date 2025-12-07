from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from validate_docbr import CPF


class WaiterBase(BaseModel):
    """Base fields for a Waiter."""

    nome: str = Field(
        ..., min_length=1, max_length=100, description="Full name of the waiter"
    )
    cpf: str = Field(..., description="CPF (11 digits, strictly validated)")
    salario: Decimal = Field(..., gt=0, decimal_places=2, description="Monthly salary")
    turno: Optional[str] = Field(
        None, max_length=20, description="Work shift (e.g., Morning, Night)"
    )
    comissao: Optional[Decimal] = Field(
        None, ge=0, decimal_places=2, description="Commission percentage"
    )

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        """
        Validates CPF using validate-docbr and sanitizes it to raw digits.
        """
        cpf_validator = CPF()
        if not cpf_validator.validate(v):
            raise ValueError("O CPF informado é inválido. Verifique os dígitos.")
        return f"{cpf_validator.mask(v)}".replace(".", "").replace("-", "")


class WaiterCreate(WaiterBase):
    """Schema for creating a new waiter."""

    pass


class WaiterResponse(WaiterBase):
    """Schema for waiter response, including DB ID."""

    id: int = Field(..., description="Unique identifier of the waiter")
    model_config = ConfigDict(from_attributes=True)