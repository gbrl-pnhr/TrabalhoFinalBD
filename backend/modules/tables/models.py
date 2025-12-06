from pydantic import BaseModel, Field, ConfigDict

class TableBase(BaseModel):
    """Base fields for a Table."""
    number: int = Field(..., gt=0, description="The visible number of the table")
    capacity: int = Field(..., gt=0, description="Number of people the table fits")
    location: str = Field(..., min_length=1, max_length=50, description="Location (e.g., Patio, Main Hall)")

class TableCreate(TableBase):
    """Schema for creating a new table."""
    pass

class TableResponse(TableBase):
    """Schema for table response, including DB ID."""
    id: int = Field(..., description="Unique identifier of the table")
    model_config = ConfigDict(from_attributes=True)