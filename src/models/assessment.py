"""
Assessment models for mental health questionnaires (PHQ-9, etc.).
"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.user import User


class AssessmentResult(BaseModel):
    """Model for storing assessment results (PHQ-9, etc.)."""

    __tablename__ = "assessment_results"

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE")
    )

    assessment_type: Mapped[str] = mapped_column(
        String(100),
        comment="Type of assessment (e.g., 'PHQ-9', 'GAD-7')"
    )

    # Используем Text для SQLite вместо JSON
    responses: Mapped[str] = mapped_column(
        Text,
        comment="User responses to assessment questions (JSON as text)"
    )

    total_score: Mapped[int] = mapped_column(
        Integer,
        comment="Calculated total score"
    )

    severity_level: Mapped[str] = mapped_column(
        String(50),
        comment="Severity level based on score"
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="assessment_results"
    )