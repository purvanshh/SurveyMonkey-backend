"""
Creator analytics router — response viewing endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.response import ResponseCountResponse, ResponseListResponse
from services import response_service

router = APIRouter(prefix="/api", tags=["responses"])


@router.get("/surveys/{survey_id}/responses/count", response_model=ResponseCountResponse)
def get_response_count(survey_id: str, db: Session = Depends(get_db)):
    """Get total response count for a survey — ideal for polling."""
    count = response_service.get_response_count(db, survey_id)
    return ResponseCountResponse(survey_id=survey_id, count=count)


@router.get("/surveys/{survey_id}/responses", response_model=ResponseListResponse)
def get_responses(survey_id: str, db: Session = Depends(get_db)):
    """Get all responses with enriched answer data for the creator dashboard."""
    responses = response_service.get_responses(db, survey_id)
    return ResponseListResponse(
        survey_id=survey_id,
        total=len(responses),
        responses=responses,
    )
