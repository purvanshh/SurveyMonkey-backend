"""Option ORM model."""

import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship

from database import Base


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class Option(Base):
    __tablename__ = "options"

    id = Column(String(36), primary_key=True, default=_generate_uuid)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(500), nullable=False, default="")
    value = Column(String(500), nullable=True, default="")
    order_index = Column(Integer, nullable=False, default=0)

    # Relationships
    question = relationship("Question", back_populates="options")

    def __repr__(self) -> str:
        return f"<Option id={self.id} label={self.label!r}>"
