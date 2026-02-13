"""Response & Answer Pydantic schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Submission (public-facing)
# ---------------------------------------------------------------------------

class AnswerSubmit(BaseModel):
    question_id: str = Field(..., description="ID of the question being answered")
    value: str | None = Field(None, description="Text answer or selected option value")
    selected_option_id: str | None = Field(None, description="Option ID for MCQ/checkbox")
    value_json: dict[str, Any] | None = Field(None, description="Extensible JSON payload")


class SurveySubmitRequest(BaseModel):
    answers: list[AnswerSubmit] = Field(..., min_length=1, description="List of answers")
    respondent_id: str | None = Field(None, description="Optional session/device identifier")
    metadata: dict[str, Any] | None = Field(None, description="IP, device info, etc.")


# ---------------------------------------------------------------------------
# Response views (creator dashboard)
# ---------------------------------------------------------------------------

class AnswerResponse(BaseModel):
    id: str
    question_id: str
    question_title: str | None = None
    question_type: str | None = None
    answer_text: str | None
    selected_option_id: str | None
    selected_option_label: str | None = None
    value_json: dict[str, Any] | None = None

    model_config = {"from_attributes": True}


class ResponseResponse(BaseModel):
    id: str
    survey_id: str
    respondent_id: str | None
    submitted_at: datetime
    answers: list[AnswerResponse] = []

    model_config = {"from_attributes": True}


class ResponseCountResponse(BaseModel):
    survey_id: str
    count: int


class ResponseListResponse(BaseModel):
    survey_id: str
    total: int
    responses: list[ResponseResponse] = []
