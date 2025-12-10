"""
Schemas for mental health assessments.
"""
from typing import List
from pydantic import Field

from src.schemas.base import BaseSchema


class AssessmentResponse(BaseSchema):
    """Response schema for assessment submission."""

    question_id: int
    response_value: int = Field(ge=0, le=3)  # Обычно 0-3 для PHQ-9


class AssessmentSubmission(BaseSchema):
    """Schema for submitting assessment responses."""

    assessment_type: str
    responses: List[AssessmentResponse]


class AssessmentResult(BaseSchema):
    """Schema for assessment results."""

    total_score: int
    severity_level: str
    recommendations: List[str]