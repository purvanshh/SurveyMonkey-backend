"""
Public survey access router — no authentication required.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.survey import SurveyResponse
from services import survey_service

router = APIRouter(prefix="/api/public", tags=["public"])


@router.get("/{share_token}", response_model=SurveyResponse)
def get_public_survey(share_token: str, db: Session = Depends(get_db)):
    """
    Retrieve full survey by share token — public endpoint.
    Returns complete hierarchy: survey → questions → options, correctly ordered.
    """
    return survey_service.get_survey_by_token(db, share_token)
