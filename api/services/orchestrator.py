from rag.retriever import retrieve_relevant_docs
from rag.generator import generate_drone_response
# We need to check if mcp_server is importing correctly. 
# The user's snippet uses: from mcp_server.server import mcp_manager
# But earlier I saw `mcp_server.server` importing `mcp_engine`. Let's check `mcp_server/server.py` content first? 
# Actually, let's just use `mcp_engine` or `mcp_manager` depending on what's in `server.py`.
# I'll optimistically assume `mcp_engine` based on `main.py` line 20: `from mcp_server.server import mcp_engine`
from mcp_server.server import mcp_engine

class DroneOrchestrator:
    """
    Orchestrates logic between RAG (Semantic search) and MCP Tools (Deterministic math).
    """
    async def process_query(self, user_query: str):
        query_lower = user_query.lower()

        # 1. Routing Logic: Check for tool-specific keywords
        # In a real scenario, you would use an LLM to extract parameters here.
        # For now, we route to RAG which explains how to use the specific tool.
        if any(word in query_lower for word in ["calculate", "roi", "profit", "break-even"]):
            # For now, simple RAG response about the tool
            return generate_drone_response(user_query)

        elif any(word in query_lower for word in ["fly", "endurance", "flight time", "battery", "range"]):
             # For now, simple RAG response about the tool
            return generate_drone_response(user_query)

        # 2. Default to RAG for general knowledge and regulations
        return generate_drone_response(user_query)

# Global instance for routes to use
drone_orchestrator = DroneOrchestrator()