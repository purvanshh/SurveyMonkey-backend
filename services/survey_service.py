"""
Survey service — all business logic for survey CRUD, questions, options, and sharing.
"""

import os
import secrets
from typing import Sequence

from sqlalchemy.orm import Session

# Frontend base URL for share links. Set FRONTEND_URL in production (e.g. https://yourapp.vercel.app).
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")


def _share_url(token: str) -> str:
    return f"{FRONTEND_URL}/s/{token}"
from fastapi import HTTPException, status

from models.survey import Survey
from models.question import Question
from models.option import Option
from schemas.survey import SurveyCreate, SurveyUpdate
from schemas.question import QuestionCreate, QuestionUpdate


# ---------------------------------------------------------------------------
# Survey CRUD
# ---------------------------------------------------------------------------

def create_survey(db: Session, data: SurveyCreate) -> Survey:
    survey = Survey(
        title=data.title,
        description=data.description or "",
        metadata_=data.metadata or {},
    )
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey


def list_surveys(db: Session) -> Sequence[Survey]:
    return db.query(Survey).order_by(Survey.created_at.desc()).all()


def get_survey(db: Session, survey_id: str) -> Survey:
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey not found")
    return survey


def update_survey(db: Session, survey_id: str, data: SurveyUpdate) -> Survey:
    survey = get_survey(db, survey_id)
    update_data = data.model_dump(exclude_unset=True)
    if "metadata" in update_data:
        update_data["metadata_"] = update_data.pop("metadata")
    for key, value in update_data.items():
        setattr(survey, key, value)
    db.commit()
    db.refresh(survey)
    return survey


def delete_survey(db: Session, survey_id: str) -> None:
    survey = get_survey(db, survey_id)
    db.delete(survey)
    db.commit()


# ---------------------------------------------------------------------------
# Share token
# ---------------------------------------------------------------------------

def generate_share_token(db: Session, survey_id: str) -> tuple[str, str]:
    """Return (share_token, share_url). Reuses existing token if present."""
    survey = get_survey(db, survey_id)
    if not survey.share_token:
        survey.share_token = secrets.token_urlsafe(16)
        db.commit()
        db.refresh(survey)
    share_url = _share_url(survey.share_token)
    return survey.share_token, share_url


def get_survey_by_token(db: Session, share_token: str) -> Survey:
    survey = db.query(Survey).filter(Survey.share_token == share_token).first()
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey not found")
    return survey


def generate_collector_link(db: Session, survey_id: str) -> dict:
    """Generate a web link collector for a survey. Reuses existing token if present."""
    survey = get_survey(db, survey_id)
    if not survey.share_token:
        survey.share_token = secrets.token_urlsafe(16)
    survey.collector_type = "web_link"
    db.commit()
    db.refresh(survey)

    from models.response import Response
    count = db.query(Response).filter(Response.survey_id == survey_id).count()

    return {
        "collector_name": "Web Link 1",
        "share_url": _share_url(survey.share_token),
        "status": "Open",
        "responses": count,
        "date_modified": survey.updated_at.strftime("%Y-%m-%d") if survey.updated_at else "",
    }


def get_collectors(db: Session, survey_id: str) -> dict:
    """Return collector metadata with live response count from DB."""
    survey = get_survey(db, survey_id)

    from models.response import Response
    count = db.query(Response).filter(Response.survey_id == survey_id).count()

    collectors = []
    if survey.share_token:
        collectors.append({
            "collector_name": "Web Link 1",
            "share_url": _share_url(survey.share_token),
            "status": "Open",
            "responses": count,
            "date_modified": survey.updated_at.strftime("%Y-%m-%d") if survey.updated_at else "",
        })

    return {
        "collectors": collectors,
        "total_responses": count,
    }


# ---------------------------------------------------------------------------
# Question CRUD
# ---------------------------------------------------------------------------

def add_question(db: Session, survey_id: str, data: QuestionCreate) -> Question:
    # Verify survey exists
    get_survey(db, survey_id)

    # Auto-assign order_index if not provided
    order_index = data.order_index
    if order_index is None:
        max_order = (
            db.query(Question.order_index)
            .filter(Question.survey_id == survey_id)
            .order_by(Question.order_index.desc())
            .first()
        )
        order_index = (max_order[0] + 1) if max_order else 0

    question = Question(
        survey_id=survey_id,
        type=data.type,
        title=data.title,
        description=data.description or "",
        required=data.required,
        order_index=order_index,
    )
    db.add(question)
    db.flush()  # Get the question.id before adding options

    # Add options
    for idx, opt_data in enumerate(data.options):
        option = Option(
            question_id=question.id,
            label=opt_data.label,
            value=opt_data.value or opt_data.label,
            order_index=opt_data.order_index if opt_data.order_index is not None else idx,
        )
        db.add(option)

    db.commit()
    db.refresh(question)
    return question


def get_question(db: Session, question_id: str) -> Question:
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


def update_question(db: Session, question_id: str, data: QuestionUpdate) -> Question:
    question = get_question(db, question_id)
    update_data = data.model_dump(exclude_unset=True)

    # Handle options replacement separately — use the original Pydantic objects
    has_new_options = "options" in update_data
    new_options_pydantic = data.options  # list[OptionCreate] or None
    update_data.pop("options", None)

    for key, value in update_data.items():
        setattr(question, key, value)

    # If options are provided, replace all existing ones
    if has_new_options and new_options_pydantic is not None:
        # Delete existing options
        db.query(Option).filter(Option.question_id == question_id).delete()
        # Add new options
        for idx, opt_data in enumerate(new_options_pydantic):
            option = Option(
                question_id=question_id,
                label=opt_data.label,
                value=opt_data.value or opt_data.label,
                order_index=opt_data.order_index if opt_data.order_index is not None else idx,
            )
            db.add(option)

    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question_id: str) -> None:
    question = get_question(db, question_id)
    db.delete(question)
    db.commit()
