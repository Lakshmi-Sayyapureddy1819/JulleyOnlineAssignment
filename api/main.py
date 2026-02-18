import sys
import os
import uuid
from datetime import datetime

# Add the project root to the python path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from rag.retriever import query_drone_knowledge, ingest_text
from mcp_server.tools.flight_calc import get_flight_estimates
from mcp_server.tools.roi_calc import get_roi_analysis
from mcp_server.tools.compliance import check_regulation_compliance
from mcp_server.tools.recommendation import recommend_drones
from mcp_server.server import mcp_engine

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

@app.get("/tools/regulation-check")
async def regulation_check(weight_kg: float, zone: str, altitude_ft: float):
    # Determine Category
    if weight_kg <= 0.25: category = "Nano"
    elif weight_kg <= 2.0: category = "Micro"
    elif weight_kg <= 25.0: category = "Small"
    else: category = "Medium/Large"

    # Core logic
    status = "✅ Compliant"
    remarks = []

    if zone.lower() == "green":
        if altitude_ft > 400:
            status = "❌ Violation"
            remarks.append("Altitude exceeds 400ft limit.")
    elif zone.lower() == "yellow":
        status = "⚠️ Restricted"
        remarks.append("ATC Permission required.")
    else:
        status = "🚫 No-Fly Zone"
        remarks.append("Red Zone: Unauthorized flight.")

    # RETURN THE KEYS THE FRONTEND EXPECTS
    return {
        "flight_status": status,      # <--- This matches your error
        "drone_category": category,
        "remarks": remarks
    }

@app.get("/tools/download-report")
async def download_report(weight: float, zone: str, alt: float, category: str, status: str):
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Add Logo (if available in project root)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_path, "logo.png")
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=8, w=30)

        # Helper to sanitize text for core fonts (Latin-1)
        def clean_text(text):
            return text.encode('latin-1', 'replace').decode('latin-1')

        # Header
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(200, 10, text=clean_text("Drone Compliance Report"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        
        # Timestamp
        pdf.set_font("Helvetica", "I", 10)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(200, 10, text=clean_text(f"Generated on: {timestamp}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(10)
        
        # Body Content
        pdf.set_font("Helvetica", size=12)
        pdf.cell(200, 10, text=clean_text(f"Drone Category: {category}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(200, 10, text=clean_text(f"Total Weight: {weight} kg"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(200, 10, text=clean_text(f"Airspace Zone: {zone}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(200, 10, text=clean_text(f"Flight Altitude: {alt} ft"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)
        
        # Status highlight
        status_clean = status.replace("✅", "").replace("❌", "").replace("⚠️", "").replace("🚫", "").strip()
        
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(200, 10, text=clean_text(f"Final Status: {status_clean}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Save file temporarily with unique name to avoid locking issues
        file_path = f"compliance_report_{uuid.uuid4()}.pdf"
        pdf.output(file_path)
        
        # Cleanup task to delete the file after sending
        def cleanup():
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return FileResponse(file_path, media_type="application/pdf", filename="Drone_Report.pdf", background=BackgroundTask(cleanup))
    except Exception as e:
        print(f"PDF Error: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"PDF Generation Failed: {str(e)}")

@app.get("/recommend/drone")
async def recommend_tool(budget: float, endurance: int):
    return recommend_drones(budget, endurance)

@app.get("/tools/recommend")
async def get_recommendation(budget: float, use: str):
    # This calls the MCP Server, which then calls the Selection Assistant
    return mcp_engine.run_tool("recommend_drone", {"max_budget": budget, "primary_use": use})

@app.get("/tools/find-drones")
async def find_drones(category: str = None):
    # This simulates a database lookup from your processed/drone_models.csv
    import pandas as pd
    try:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_path, "data", "processed", "drone_models.csv")
        df = pd.read_csv(data_path)
        if category:
            # Filter drones by category (Nano, Micro, etc.)
            # Using 'class' column as per data generation script
            filtered_df = df[df['class'].str.lower() == category.lower()]
            return filtered_df.to_dict(orient="records")
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

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