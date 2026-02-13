"""Question ORM model."""

import uuid

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship

from database import Base


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=_generate_uuid)
    survey_id = Column(String(36), ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(50), nullable=False, default="multiple_choice")
    title = Column(Text, nullable=False, default="")
    description = Column(Text, nullable=True, default="")
    required = Column(Boolean, nullable=False, default=False)
    order_index = Column(Integer, nullable=False, default=0)

    # Relationships
    survey = relationship("Survey", back_populates="questions")
    options = relationship(
        "Option",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="Option.order_index",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Question id={self.id} type={self.type!r}>"
