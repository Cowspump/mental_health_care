"""
Base model with common fields and functionality.
"""
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BaseModel(Base):
    """
    Abstract base model with common fields.
    Provides UUID primary key and timestamp tracking.
    """

    __abstract__ = True

    # Используем String вместо UUID для SQLite
    id: Mapped[str] = mapped_column(
        String(36),  # UUID как строка
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        comment="Unique identifier"
    )

    # Автоматические timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        comment="Record creation timestamp"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        comment="Record last update timestamp"
    )

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<{self.__class__.__name__}(id={self.id})>"