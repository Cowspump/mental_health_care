"""
Journal entry model for daily thoughts and mood tracking.
"""
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.user import User


class JournalEntry(BaseModel):
    """
    Journal entry model for storing user's daily thoughts and mood.
    Core entity for the journaling feature.
    """

    __tablename__ = "journal_entries"

    # Foreign key к пользователю
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        comment="User who created this entry"
    )

    # Заголовок записи
    title: Mapped[str] = mapped_column(
        String(255),
        comment="Entry title"
    )

    # Основной контент
    content: Mapped[str] = mapped_column(
        Text,
        comment="Journal entry content"
    )

    # Дата записи (может отличаться от created_at)
    entry_date: Mapped[date] = mapped_column(
        Date,
        comment="Date this entry refers to"
    )

    # Настроение от 1 до 10
    mood_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Mood rating from 1 (very bad) to 10 (excellent)"
    )

    # Уровень энергии от 1 до 10
    energy_level: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Energy level from 1 (very low) to 10 (very high)"
    )

    # Теги для категоризации
    tags: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Comma-separated tags for categorization"
    )

    # Relationship back to user
    user: Mapped["User"] = relationship(
        "User",
        back_populates="journal_entries"
    )

    def __str__(self) -> str:
        """String representation for display."""
        return f"{self.title} ({self.entry_date})"