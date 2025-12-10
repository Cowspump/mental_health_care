"""
Base schemas for common patterns.
Provides consistent structure across all API responses.
"""
from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

DataT = TypeVar('DataT')


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        # Позволяет использовать ORM модели напрямую
        from_attributes=True,
        # Валидация при присвоении значений
        validate_assignment=True,
        # Использовать enum values вместо имён
        use_enum_values=True,
    )


class TimestampMixin(BaseModel):
    """Mixin for models with timestamp fields."""
    created_at: datetime
    updated_at: datetime


class UUIDMixin(BaseModel):
    """Mixin for models with UUID primary key."""
    id: str


class PaginationParams(BaseModel):
    """Standard pagination parameters."""
    skip: int = 0
    limit: int = 100


class PaginatedResponse(BaseModel, Generic[DataT]):
    """Standard paginated response format."""
    items: List[DataT]
    total: int
    skip: int
    limit: int
    has_next: bool

    @classmethod
    def create(
            cls,
            items: List[DataT],
            total: int,
            skip: int,
            limit: int,
    ) -> "PaginatedResponse[DataT]":
        """Factory method for creating paginated responses."""
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            has_next=skip + limit < total,
        )


class ErrorResponse(BaseModel):
    """Standard error response format."""
    detail: str
    error_code: Optional[str] = None