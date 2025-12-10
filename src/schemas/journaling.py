"""
Pydantic schemas for journaling API endpoints.
Defines request/response models for journal entries.
"""
from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from src.schemas.base import BaseSchema, TimestampMixin, UUIDMixin


class JournalEntryBase(BaseSchema):
    """Base schema for journal entry with common fields."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Entry title"
    )

    content: str = Field(
        ...,
        min_length=1,
        description="Journal entry content"
    )

    entry_date: date = Field(
        ...,
        description="Date this entry refers to"
    )

    mood_rating: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="Mood rating from 1 (very bad) to 10 (excellent)"
    )

    energy_level: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="Energy level from 1 (very low) to 10 (very high)"
    )

    tags: Optional[str] = Field(
        None,
        max_length=500,
        description="Comma-separated tags for categorization"
    )


class JournalEntryCreate(JournalEntryBase):
    """Schema for creating new journal entries."""
    pass


class JournalEntryUpdate(BaseSchema):
    """
    Schema for updating existing journal entries.
    All fields are optional for partial updates.
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Entry title"
    )

    content: Optional[str] = Field(
        None,
        min_length=1,
        description="Journal entry content"
    )

    entry_date: Optional[date] = Field(
        None,
        description="Date this entry refers to"
    )

    mood_rating: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="Mood rating from 1 (very bad) to 10 (excellent)"
    )

    energy_level: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="Energy level from 1 (very low) to 10 (very high)"
    )

    tags: Optional[str] = Field(
        None,
        max_length=500,
        description="Comma-separated tags for categorization"
    )


class JournalEntryResponse(JournalEntryBase, UUIDMixin, TimestampMixin):
    """Schema for journal entry responses."""

    user_id: str = Field(..., description="ID of the user who created this entry")


class JournalStatsResponse(BaseSchema):
    """Response schema for journal statistics."""

    total_entries: int
    entries_this_month: int
    average_mood_this_month: Optional[float] = None
    average_energy_this_month: Optional[float] = None
    most_used_tags: List[str]
    mood_trend: List[dict]  # [{"date": "2024-01-01", "mood": 7.5}]