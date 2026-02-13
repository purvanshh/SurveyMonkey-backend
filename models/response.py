"""Response ORM model."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


def _generate_uuid() -> str:
    return str(uuid.uuid4())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Response(Base):
    __tablename__ = "responses"

    id = Column(String(36), primary_key=True, default=_generate_uuid)
    survey_id = Column(String(36), ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_at = Column(DateTime(timezone=True), default=_utcnow, nullable=False)
    respondent_id = Column(String(255), nullable=True, index=True)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    # Relationships
    survey = relationship("Survey", back_populates="responses")
    answers = relationship(
        "Answer",
        back_populates="response",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Response id={self.id} survey_id={self.survey_id}>"