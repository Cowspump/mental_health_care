"""
FastAPI router for journaling endpoints.
Handles HTTP requests and delegates business logic to service layer.
"""
from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from src.api.deps import get_current_user_id, get_journaling_service, validate_uuid
from src.schemas.journaling import (
    JournalEntryCreate,
    JournalEntryResponse,
    JournalEntryUpdate,
    JournalStatsResponse
)
from src.services.journaling import JournalingService

# Создаём роутер для journaling endpoints
router = APIRouter(prefix="/journal", tags=["journaling"])


@router.post(
    "/entries",
    response_model=JournalEntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new journal entry",
    description="Create a new journal entry for the authenticated user."
)
async def create_journal_entry(
        entry_data: JournalEntryCreate,
        current_user_id: UUID = Depends(get_current_user_id),
        journaling_service: JournalingService = Depends(get_journaling_service),
) -> JournalEntryResponse:
    """
    Create a new journal entry.

    - **title**: Entry title (required)
    - **content**: Entry content (required)
    - **entry_date**: Date this entry refers to (required)
    - **mood_rating**: Mood rating from 1-10 (optional)
    - **energy_level**: Energy level from 1-10 (optional)
    - **tags**: Comma-separated tags (optional)
    """
    try:
        entry = await journaling_service.create_entry(current_user_id, entry_data)
        return JournalEntryResponse.model_validate(entry)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create journal entry: {str(e)}"
        )


@router.get(
    "/entries",
    response_model=List[JournalEntryResponse],
    summary="Get journal entries",
    description="Get paginated list of journal entries with optional filtering."
)
async def get_journal_entries(
        skip: int = Query(0, ge=0, description="Number of entries to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Maximum entries to return"),
        from_date: Optional[date] = Query(None, description="Filter from this date"),
        to_date: Optional[date] = Query(None, description="Filter to this date"),
        tags: Optional[str] = Query(None, description="Filter by tags"),
        current_user_id: UUID = Depends(get_current_user_id),
        journaling_service: JournalingService = Depends(get_journaling_service),
) -> List[JournalEntryResponse]:
    """
    Get user's journal entries with optional filtering and pagination.

    Query parameters:
    - **skip**: Number of entries to skip for pagination
    - **limit**: Maximum number of entries to return (1-1000)
    - **from_date**: Filter entries from this date (YYYY-MM-DD)
    - **to_date**: Filter entries to this date (YYYY-MM-DD)
    - **tags**: Filter by tags (partial match)
    """
    try:
        entries = await journaling_service.get_user_entries(
            user_id=current_user_id,
            skip=skip,
            limit=limit,
            from_date=from_date,
            to_date=to_date,
            tags=tags
        )
        return [JournalEntryResponse.model_validate(entry) for entry in entries]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve journal entries: {str(e)}"
        )


@router.get(
    "/entries/{entry_id}",
    response_model=JournalEntryResponse,
    summary="Get a specific journal entry",
    description="Retrieve a specific journal entry by ID."
)
async def get_journal_entry(
        entry_id: str,
        current_user_id: UUID = Depends(get_current_user_id),
        journaling_service: JournalingService = Depends(get_journaling_service),
) -> JournalEntryResponse:
    """
    Get a specific journal entry by ID.

    - **entry_id**: UUID of the journal entry to retrieve
    """
    # Валидируем UUID
    entry_uuid = validate_uuid(entry_id)

    try:
        entry = await journaling_service.get_entry(current_user_id, entry_uuid)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal entry not found"
            )

        return JournalEntryResponse.model_validate(entry)
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve journal entry: {str(e)}"
        )


@router.put(
    "/entries/{entry_id}",
    response_model=JournalEntryResponse,
    summary="Update a journal entry",
    description="Update an existing journal entry."
)
async def update_journal_entry(
        entry_id: str,
        update_data: JournalEntryUpdate,
        current_user_id: UUID = Depends(get_current_user_id),
        journaling_service: JournalingService = Depends(get_journaling_service),
) -> JournalEntryResponse:
    """
    Update an existing journal entry.

    - **entry_id**: UUID of the journal entry to update
    - All fields in the request body are optional for partial updates
    """
    # Валидируем UUID
    entry_uuid = validate_uuid(entry_id)

    try:
        updated_entry = await journaling_service.update_entry(
            current_user_id, entry_uuid, update_data
        )

        if not updated_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal entry not found"
            )

        return JournalEntryResponse.model_validate(updated_entry)
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update journal entry: {str(e)}"
        )


@router.delete(
    "/entries/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a journal entry",
    description="Delete an existing journal entry."
)
async def delete_journal_entry(
        entry_id: str,
        current_user_id: UUID = Depends(get_current_user_id),
        journaling_service: JournalingService = Depends(get_journaling_service),
):
    """
    Delete a journal entry.

    - **entry_id**: UUID of the journal entry to delete
    """
    # Валидируем UUID
    entry_uuid = validate_uuid(entry_id)

    try:
        deleted = await journaling_service.delete_entry(current_user_id, entry_uuid)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal entry not found"
            )

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content=None
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete journal entry: {str(e)}"
        )


@router.get(
    "/stats",
    response_model=JournalStatsResponse,
    summary="Get journal statistics",
    description="Get statistics and analytics for user's journal entries."
)
async def get_journal_stats(
        current_user_id: UUID = Depends(get_current_user_id),
        journaling_service: JournalingService = Depends(get_journaling_service),
) -> JournalStatsResponse:
    """
    Get comprehensive statistics for user's journal entries.

    Returns statistics including:
    - Total number of entries
    - Entries this month
    - Average mood and energy levels
    - Mood trends over time
    - Most used tags
    """
    try:
        stats = await journaling_service.get_user_stats(current_user_id)
        return JournalStatsResponse.model_validate(stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve journal statistics: {str(e)}"
        )