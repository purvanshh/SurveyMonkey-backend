"""
Pydantic schemas for Answers.
"""

from pydantic import BaseModel, ConfigDict
from typing import Any


class AnswerBase(BaseModel):
    question_id: str
    answer_text: str | None = None
    selected_option_id: str | None = None
    value_json: dict | list | None = None


class AnswerCreate(AnswerBase):
    pass


class AnswerResponse(AnswerBase):
    model_config = ConfigDict(from_attributes=True)

    id: str





class AnswerForResponse(AnswerBase):


    model_config = ConfigDict(from_attributes=True)





    id: str


    question: "QuestionResponse"








from .question import QuestionResponse





AnswerForResponse.model_rebuild()

