from mcp_server.tools.flight_calc import get_flight_estimates
from mcp_server.tools.roi_calc import get_roi_analysis
from mcp_server.tools.selection_assistant import recommend_drone

class DroneMCPServer:
    """
    The Model Context Protocol server that manages all specialized drone tools.
    """
    def __init__(self):
        self.name = "IndiaDroneIntel-Server"

    def run_tool(self, tool_name: str, params: dict):
        if tool_name == "calculate_flight":
            return get_flight_estimates(**params)
        elif tool_name == "calculate_roi":
            return get_roi_analysis(**params)
        elif tool_name == "recommend_drone":
            return recommend_drone(**params)
        else:
            return {"error": "Tool not found"}

# Initialize a global instance for the API to use
mcp_engine = DroneMCPServer()