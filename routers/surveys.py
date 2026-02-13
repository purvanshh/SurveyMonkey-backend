"""
Survey and Question API routers.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.survey import (
    SurveyCreate,
    SurveyUpdate,
    SurveyResponse,
    SurveyListResponse,
    SurveyShareResponse,
)
from schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse
from services import survey_service

router = APIRouter(prefix="/api", tags=["surveys"])


# ---------------------------------------------------------------------------
# Survey endpoints
# ---------------------------------------------------------------------------

@router.post("/surveys", response_model=SurveyResponse, status_code=201)
def create_survey(data: SurveyCreate, db: Session = Depends(get_db)):
    """Create a new survey container."""
    return survey_service.create_survey(db, data)


@router.get("/surveys", response_model=list[SurveyListResponse])
def list_surveys(db: Session = Depends(get_db)):
    """List all surveys (most recent first)."""
    return survey_service.list_surveys(db)


@router.get("/surveys/{survey_id}", response_model=SurveyResponse)
def get_survey(survey_id: str, db: Session = Depends(get_db)):
    """Get full survey with all questions and options."""
    return survey_service.get_survey(db, survey_id)


@router.patch("/surveys/{survey_id}", response_model=SurveyResponse)
def update_survey(survey_id: str, data: SurveyUpdate, db: Session = Depends(get_db)):
    """Update survey metadata (title, description, settings)."""
    return survey_service.update_survey(db, survey_id, data)


@router.delete("/surveys/{survey_id}", status_code=204)
def delete_survey(survey_id: str, db: Session = Depends(get_db)):
    """Delete a survey and all its questions/options."""
    survey_service.delete_survey(db, survey_id)


@router.post("/surveys/{survey_id}/share", response_model=SurveyShareResponse)
def share_survey(survey_id: str, db: Session = Depends(get_db)):
    """Generate (or return existing) shareable link for a survey."""
    token, url = survey_service.generate_share_token(db, survey_id)
    return SurveyShareResponse(share_token=token, share_url=url)


@router.post("/surveys/{survey_id}/generate-link")
def generate_collector_link(survey_id: str, db: Session = Depends(get_db)):
    """Generate a web link collector for the survey."""
    return survey_service.generate_collector_link(db, survey_id)


@router.get("/surveys/{survey_id}/collectors")
def get_collectors(survey_id: str, db: Session = Depends(get_db)):
    """Get all collectors for a survey with live response counts."""
    return survey_service.get_collectors(db, survey_id)


# ---------------------------------------------------------------------------
# Question endpoints
# ---------------------------------------------------------------------------

@router.post("/surveys/{survey_id}/questions", response_model=QuestionResponse, status_code=201)
def add_question(survey_id: str, data: QuestionCreate, db: Session = Depends(get_db)):
    """Add a question to a survey."""
    return survey_service.add_question(db, survey_id, data)


@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question(question_id: str, data: QuestionUpdate, db: Session = Depends(get_db)):
    """Update a question (and optionally replace its options)."""
    return survey_service.update_question(db, question_id, data)


@router.delete("/questions/{question_id}", status_code=204)
def delete_question(question_id: str, db: Session = Depends(get_db)):
    """Delete a question and all its options."""
    survey_service.delete_question(db, question_id)
