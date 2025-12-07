from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from validate_docbr import CPF


class ChefBase(BaseModel):
    """Base fields for a Chef."""

    nome: str = Field(
        ..., min_length=1, max_length=100, description="Full name of the chef"
    )
    cpf: str = Field(..., description="CPF (11 digits, strictly validated)")
    salario: Decimal = Field(..., gt=0, decimal_places=2, description="Monthly salary")
    especialidade: Optional[str] = Field(
        None, max_length=50, description="Culinary specialty"
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


class ChefCreate(ChefBase):
    """Schema for creating a new chef."""

    pass


class ChefResponse(ChefBase):
    """Schema for chef response, including DB ID."""

    id: int = Field(..., description="Unique identifier of the chef")
    model_config = ConfigDict(from_attributes=True)