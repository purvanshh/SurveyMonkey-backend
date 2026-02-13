"""
Response service — business logic for survey submissions and analytics.
"""

from typing import Sequence

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.response import Response
from models.answer import Answer
from models.question import Question
from models.option import Option
from schemas.response import SurveySubmitRequest, AnswerResponse, ResponseResponse


def submit_response(db: Session, survey_id: str, data: SurveySubmitRequest) -> Response:
    """Atomically create a Response and all its Answers."""
    response = Response(
        survey_id=survey_id,
        respondent_id=data.respondent_id,
        metadata_=data.metadata or {},
    )
    db.add(response)
    db.flush()  # Get response.id

    for ans in data.answers:
        # Determine answer_text: use value directly, or look up option label
        answer_text = ans.value
        selected_option_id = ans.selected_option_id

        # If selected_option_id provided but no text, look up the option label
        if selected_option_id and not answer_text:
            option = db.query(Option).filter(Option.id == selected_option_id).first()
            if option:
                answer_text = option.label

        answer = Answer(
            response_id=response.id,
            question_id=ans.question_id,
            answer_text=answer_text,
            selected_option_id=selected_option_id,
            value_json=ans.value_json,
        )
        db.add(answer)

    db.commit()
    db.refresh(response)
    return response


def get_response_count(db: Session, survey_id: str) -> int:
    return db.query(Response).filter(Response.survey_id == survey_id).count()


def get_responses(db: Session, survey_id: str) -> list[ResponseResponse]:
    """Get all responses for a survey with enriched answer data."""
    responses = (
        db.query(Response)
        .filter(Response.survey_id == survey_id)
        .order_by(Response.submitted_at.desc())
        .all()
    )

    result = []
    for resp in responses:
        enriched_answers = []
        for ans in resp.answers:
            # Enrich with question info
            question = ans.question
            option = ans.selected_option

            enriched_answers.append(AnswerResponse(
                id=ans.id,
                question_id=ans.question_id,
                question_title=question.title if question else None,
                question_type=question.type if question else None,
                answer_text=ans.answer_text,
                selected_option_id=ans.selected_option_id,
                selected_option_label=option.label if option else None,
                value_json=ans.value_json,
            ))

        result.append(ResponseResponse(
            id=resp.id,
            survey_id=resp.survey_id,
            respondent_id=resp.respondent_id,
            submitted_at=resp.submitted_at,
            answers=enriched_answers,
        ))

    return result
