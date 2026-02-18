from rag.generator import generate_drone_response
# from mcp_server.server import mcp_manager 

class DroneOrchestrator:
    """
    Orchestrates logic between RAG (Semantic search) and MCP Tools (Deterministic math).
    """
    async def process_query(self, user_query: str):
        query_lower = user_query.lower()

        # 1. Routing Logic: Detect intent for calculation tools
        if any(word in query_lower for word in ["calculate", "roi", "profit", "break-even"]):
            # Direct the user to the Analytics tab or provide RAG guidance on the tool
            return generate_drone_response(user_query)
        elif any(word in query_lower for word in ["flight", "endurance", "battery", "range"]):
            # Logic to explain flight estimation or trigger calculations
            return generate_drone_response(user_query)

        # 2. Defaullsexting retrieval logic from retriever.py
        return generate_drone_response(user_query)

# Global instance for routes to use=