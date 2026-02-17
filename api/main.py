import sys
import os

# Add the project root to the python path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from rag.retriever import query_drone_knowledge, ingest_text
from mcp_server.tools.flight_calc import get_flight_estimates
from mcp_server.tools.roi_calc import get_roi_analysis
from mcp_server.tools.compliance import check_regulation_compliance
from mcp_server.tools.recommendation import recommend_drones

app = FastAPI(title="India Drone Intel API")

class ChatInput(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(input_data: ChatInput):
    return query_drone_knowledge(input_data.prompt)

@app.get("/calculate/flight")
async def flight_tool(bat: float, weight: float, pay: float):
    return get_flight_estimates(bat, weight, pay)

@app.get("/calculate/roi")
async def roi_tool(inv: float, rev: float):
    return get_roi_analysis(inv, rev)

@app.get("/check/compliance")
async def compliance_tool(weight: float, zone: str, alt: float, purpose: str = "Recreational"):
    return check_regulation_compliance(weight, zone, alt, purpose)

@app.get("/recommend/drone")
async def recommend_tool(budget: float, endurance: int):
    return recommend_drones(budget, endurance)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    chunks = ingest_text(text, file.filename)
    return {"message": "Document processed successfully", "chunks_added": chunks}

@app.get("/analytics")
async def analytics():
    return {"status": "System Operational", "active_modules": ["RAG", "Flight Calc", "ROI Calc", "Compliance", "Recommendation"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)