"""
Router for first aid/emergency resources.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/first-aid", tags=["first-aid"])


@router.get("/resources")
async def get_first_aid_resources():
    """Get emergency mental health resources."""
    return {
        "emergency_contacts": [
            {
                "name": "National Suicide Prevention Lifeline",
                "phone": "988",
                "description": "24/7 crisis support"
            }
        ],
        "coping_strategies": [
            {
                "title": "Deep Breathing",
                "description": "Take slow, deep breaths for 5 minutes",
                "steps": ["Inhale for 4 seconds", "Hold for 4 seconds", "Exhale for 6 seconds"]
            }
        ]
    }