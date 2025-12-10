"""
Stub router for monitoring and analytics.
"""
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/dashboard")
async def get_dashboard_data():
    """Get dashboard data for monitoring."""
    return {
        "mood_trend": [],
        "productivity_metrics": {},
        "weekly_summary": {}
    }