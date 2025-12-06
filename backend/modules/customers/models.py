from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr

class CustomerBase(BaseModel):
    """Base fields for a Customer."""
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the customer")
    phone: Optional[str] = Field(None, max_length=20, description="Contact phone number")
    email: EmailStr = Field(..., max_length=100, description="Email address")

class CustomerCreate(CustomerBase):
    """Schema for creating a new customer."""
    pass

class CustomerResponse(CustomerBase):
    """Schema for customer response, including DB ID."""
    id: int = Field(..., description="Unique identifier of the customer")
    model_config = ConfigDict(from_attributes=True)