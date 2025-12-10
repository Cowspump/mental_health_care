"""
FastAPI dependencies for common functionality.
Provides reusable dependencies for authentication, database, etc.
"""
import uuid
from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db


# Stub для аутентификации - в production заменить на реальную
async def get_current_user_id() -> str:
    """
    Stub for user authentication.
    In production, this would decode JWT token and return actual user ID.

    Returns:
        Mock user ID for development
    """
    # В реальном приложении здесь будет декодирование JWT токена
    # и получение user_id из claims
    return str(uuid.uuid4())  # Mock user ID для демо


async def get_current_user_id_optional() -> str | None:
    """
    Optional authentication dependency.
    Returns None if user is not authenticated.
    """
    try:
        return await get_current_user_id()
    except HTTPException:
        return None


def get_journaling_service(
        db: AsyncSession = Depends(get_db)
) -> "JournalingService":
    """
    Dependency to get journaling service instance.

    Args:
        db: Database session from dependency

    Returns:
        JournalingService instance
    """
    from src.services.journaling import JournalingService
    return JournalingService(db)


def get_assessment_service(
        db: AsyncSession = Depends(get_db)
) -> "AssessmentService":
    """Dependency to get assessment service instance."""
    from src.services.assessment import AssessmentService
    return AssessmentService(db)


# Общие валидаторы
def validate_uuid(uuid_str: str) -> str:
    """
    Validate UUID string format.

    Args:
        uuid_str: String representation of UUID

    Returns:
        UUID string if valid

    Raises:
        HTTPException: If UUID is invalid
    """
    try:
        # Проверяем что это валидный UUID
        uuid.UUID(uuid_str)
        return uuid_str
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )