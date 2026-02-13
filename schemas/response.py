"""
Pydantic schemas for Responses.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

from .answer import AnswerResponse, AnswerCreate


class ResponseBase(BaseModel):
    respondent_id: Optional[str] = None
    metadata_: Optional[dict] = None


class ResponseCreate(ResponseBase):
    answers: List[AnswerCreate]


class SurveySubmitRequest(ResponseBase):
    answers: List[AnswerCreate]


class ResponseResponse(ResponseBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    submitted_at: datetime
    answers: List[AnswerResponse]


class ResponseCountResponse(BaseModel):
    survey_id: str
    count: int


class ResponseListResponse(BaseModel):
    survey_id: str
    total: int
    responses: List[ResponseResponse]
