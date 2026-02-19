from fastapi import APIRouter, HTTPException
from api.models.schemas import ChatRequest, ChatResponse
from api.services.orchestrator import drone_orchestrator

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(input_data: ChatRequest):
    """
    Main entry point for AI communication.
    Routes queries to the Orchestrator for RAG or Tool selection.
    """
    try:
        # Pass the prompt to the service layer
        result = await drone_orchestrator.process_query(input_data.prompt)
        
        # Ensure result matches response model
        # orchestrator returns dict with "answer" and "sources"
        return ChatResponse(
            answer=result.get("answer", "No answer generated."),
            sources=result.get("sources", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat Error: {str(e)}")