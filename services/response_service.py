"""
Response service — business logic for survey responses and answers.
"""

from sqlalchemy.orm import Session, joinedload
from typing import Sequence

from models.response import Response
from models.answer import Answer
from schemas.response import ResponseCreate, SurveySubmitRequest


def submit_response(db: Session, survey_id: str, data: ResponseCreate | SurveySubmitRequest) -> Response:
    """
    Create a new response and its associated answers.
    This is an atomic operation.
    """
    response = Response(
        survey_id=survey_id,
        respondent_id=data.respondent_id,
        metadata_=data.metadata_ or {},
    )
    db.add(response)
    db.flush()  # Flush to get the response.id

    for answer_data in data.answers:
        answer = Answer(
            response_id=response.id,
            question_id=answer_data.question_id,
            answer_text=answer_data.answer_text,
            selected_option_id=answer_data.selected_option_id,
            value_json=answer_data.value_json,
        )
        db.add(answer)

    db.commit()
    db.refresh(response)
    return response


def get_responses(db: Session, survey_id: str) -> Sequence[Response]:
    """
    Get all responses for a survey, with answers and questions eagerly loaded.
    """
    return (
        db.query(Response)
        .filter(Response.survey_id == survey_id)
        .options(
            joinedload(Response.answers)
            .joinedload(Answer.question)
        )
        .order_by(Response.submitted_at.desc())
        .all()
    )


def get_response_count(db: Session, survey_id: str) -> int:
    """
    Get the total number of responses for a survey.
    """
    return db.query(Response).filter(Response.survey_id == survey_id).count()