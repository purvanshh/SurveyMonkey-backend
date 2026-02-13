"""
Hosted survey router — public runtime endpoints for live surveys.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.survey import SurveyResponse
from schemas.response import SurveySubmitRequest, ResponseResponse
from services import survey_service
from services import response_service

router = APIRouter(prefix="/s", tags=["hosted"])


@router.get("/{share_token}", response_model=SurveyResponse)
def get_hosted_survey(share_token: str, db: Session = Depends(get_db)):
    """
    Load hosted survey for respondents.
    Returns full survey structure for rendering the live survey form.
    """
    return survey_service.get_survey_by_token(db, share_token)


@router.post("/{share_token}/submit", response_model=ResponseResponse, status_code=201)
def submit_survey(share_token: str, data: SurveySubmitRequest, db: Session = Depends(get_db)):
    """
    Submit a survey response.
    Atomically persists all answers — no partial saves.
    """
    survey = survey_service.get_survey_by_token(db, share_token)
    response = response_service.submit_response(db, survey.id, data)

    # Re-fetch with enriched data
    enriched = response_service.get_responses(db, survey.id)
    # Return just the one we created
    for r in enriched:
        if r.id == response.id:
            return r

    # Fallback — should never reach here
    return ResponseResponse(
        id=response.id,
        survey_id=response.survey_id,
        respondent_id=response.respondent_id,
        submitted_at=response.submitted_at,
        answers=[],
    )
