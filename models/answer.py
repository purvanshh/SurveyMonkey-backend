"""Answer ORM model."""

import uuid

from sqlalchemy import Column, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class Answer(Base):
    __tablename__ = "answers"

    id = Column(String(36), primary_key=True, default=_generate_uuid)
    response_id = Column(String(36), ForeignKey("responses.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    answer_text = Column(Text, nullable=True)
    selected_option_id = Column(String(36), ForeignKey("options.id"), nullable=True, index=True)
    value_json = Column(JSON, nullable=True)

    # Relationships
    response = relationship("Response", back_populates="answers")
    question = relationship("Question", lazy="selectin")
    selected_option = relationship("Option", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Answer id={self.id} question_id={self.question_id}>"