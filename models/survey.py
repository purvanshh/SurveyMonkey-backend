"""Survey ORM model."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, JSON, Index
from sqlalchemy.orm import relationship

from database import Base


def _generate_uuid() -> str:
    return str(uuid.uuid4())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Survey(Base):
    __tablename__ = "surveys"

    id = Column(String(36), primary_key=True, default=_generate_uuid)
    title = Column(String(255), nullable=False, default="Untitled")
    description = Column(Text, nullable=True, default="")
    share_token = Column(String(64), unique=True, nullable=True, index=True)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False)

    # Relationships
    questions = relationship(
        "Question",
        back_populates="survey",
        cascade="all, delete-orphan",
        order_by="Question.order_index",
        lazy="selectin",
    )
    responses = relationship(
        "Response",
        back_populates="survey",
        cascade="all, delete-orphan",
        order_by="Response.submitted_at.desc()",
        lazy="noload",
    )

    def __repr__(self) -> str:
        return f"<Survey id={self.id} title={self.title!r}>"
