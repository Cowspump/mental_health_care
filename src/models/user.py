"""
User model for authentication and profile management.
"""
from typing import List, TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.journal import JournalEntry
    from src.models.assessment import AssessmentResult


class User(BaseModel):
    """
    User model for platform authentication and profile.
    In production, you'd add proper authentication fields.
    """

    __tablename__ = "users"

    # Основные поля пользователя
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        comment="User email address"
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        comment="User full name"
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="User biography or notes"
    )

    # Relationships (обратные связи с другими моделями)
    journal_entries: Mapped[List["JournalEntry"]] = relationship(
        "JournalEntry",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    assessment_results: Mapped[List["AssessmentResult"]] = relationship(
        "AssessmentResult",
        back_populates="user",
        cascade="all, delete-orphan"
    )