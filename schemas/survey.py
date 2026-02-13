"""Survey Pydantic schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .question import QuestionResponse


class SurveyCreate(BaseModel):
    title: str = Field("Untitled", min_length=1, max_length=255, description="Survey title")
    description: str | None = Field(None, description="Optional description")
    metadata: dict[str, Any] | None = Field(None, description="Extensible JSON for layout, style, settings")


class SurveyUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    metadata: dict[str, Any] | None = None


class SurveyResponse(BaseModel):
    id: str
    title: str
    description: str | None
    share_token: str | None
    metadata: dict[str, Any] | None = Field(None, alias="metadata_")
    created_at: datetime
    updated_at: datetime
    questions: list[QuestionResponse] = []

    model_config = {"from_attributes": True, "populate_by_name": True}


class SurveyListResponse(BaseModel):
    id: str
    title: str
    description: str | None
    share_token: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SurveyShareResponse(BaseModel):
    share_token: str
    share_url: str
