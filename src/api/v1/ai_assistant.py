"""
Stub router for AI assistant functionality.
"""
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/ai", tags=["ai-assistant"])


@router.post("/chat")
async def chat_with_ai(
    # TODO: Add proper request schema for chat messages
):
    """Chat with AI assistant."""
    # TODO: Integrate with LLM service (OpenAI, Claude, etc.)
    return {
        "response": "This is a placeholder AI response. Integration with actual LLM needed.",
        "conversation_id": "placeholder-id"
    }


@router.get("/conversations")
async def get_conversations():
    """Get user's conversation history."""
    return {"conversations": []}