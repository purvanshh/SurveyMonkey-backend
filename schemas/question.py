"""Question Pydantic schemas."""

from pydantic import BaseModel, Field

from .option import OptionCreate, OptionResponse


class QuestionCreate(BaseModel):
    type: str = Field("multiple_choice", description="Question type: multiple_choice, text, checkbox, dropdown, star_rating, matrix, slider, ranking")
    title: str = Field(..., min_length=1, description="Question text displayed to respondent")
    description: str | None = Field(None, description="Optional secondary description or help text")
    required: bool = Field(False, description="Whether an answer is required")
    order_index: int | None = Field(None, ge=0, description="Position within the survey; auto-assigned if omitted")
    options: list[OptionCreate] = Field(default_factory=list, description="Answer options (for MCQ, checkbox, dropdown types)")


class QuestionUpdate(BaseModel):
    type: str | None = None
    title: str | None = None
    description: str | None = None
    required: bool | None = None
    order_index: int | None = None
    options: list[OptionCreate] | None = Field(None, description="If provided, replaces all existing options")


class QuestionResponse(BaseModel):
    id: str
    survey_id: str
    type: str
    title: str
    description: str | None
    required: bool
    order_index: int
    options: list[OptionResponse] = []

    model_config = {"from_attributes": True}
