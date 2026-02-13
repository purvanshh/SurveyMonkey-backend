"""Option Pydantic schemas."""

from pydantic import BaseModel, Field


class OptionCreate(BaseModel):
    label: str = Field(..., min_length=1, max_length=500, description="Display label for this option")
    value: str | None = Field(None, max_length=500, description="Optional machine-readable value")
    order_index: int | None = Field(None, ge=0, description="Position within the question; auto-assigned if omitted")


class OptionResponse(BaseModel):
    id: str
    question_id: str
    label: str
    value: str | None
    order_index: int

    model_config = {"from_attributes": True}
