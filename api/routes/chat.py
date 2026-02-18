from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.services.orchestrator import drone_orchestrator

router = APIRouter()

class ChatInput(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_endpoint(input_data: ChatInput):
    """
    Handles AI communication by routing queries to the Orchestrator.
    """
    try:
        # Pass the prompt to the service layer
        response = await drone_orchestrator.process_query(input_data.prompt)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat Error: {str(e)}")