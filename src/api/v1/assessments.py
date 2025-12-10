"""
Stub router for mental health assessments.
"""
from fastapi import APIRouter, Depends

from src.api.deps import get_current_user_id, get_assessment_service

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.get("/available")
async def get_available_assessments(
    assessment_service = Depends(get_assessment_service)
):
    """Get list of available mental health assessments."""
    return await assessment_service.get_available_assessments()


@router.post("/{assessment_type}/submit")
async def submit_assessment(
    assessment_type: str,
    # TODO: Add proper request schema
    current_user_id = Depends(get_current_user_id),
    assessment_service = Depends(get_assessment_service)
):
    """Submit assessment responses."""
    # TODO: Implement assessment submission
    return {"message": "Assessment submitted successfully"}