import os
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from fpdf import FPDF
from fpdf.enums import XPos, YPos

from api.models.schemas import ComplianceRequest, RecommendRequestSimple
from mcp_server.server import mcp_engine
from mcp_server.tools.flight_calc import get_flight_estimates
from mcp_server.tools.roi_calc import get_roi_analysis
from mcp_server.tools.compliance import check_regulation_compliance

router = APIRouter()

# Helper to sanitize text for core fonts (Latin-1)
def clean_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

@router.get("/calculate/flight")
async def flight_tool(bat: float, weight: float, pay: float, wind: str = "Calm"):
    return get_flight_estimates(bat, weight, pay, wind)

@router.get("/calculate/roi")
async def roi_tool(inv: float, rev: float, op_costs: float = 2500, use_case: str = "General"):
    return get_roi_analysis(inv, rev, op_costs, use_case)

@router.get("/check/compliance")
async def compliance_tool(params: ComplianceRequest = Depends()):
    return check_regulation_compliance(params.weight_kg, params.zone, params.altitude_ft, params.purpose)

@router.get("/tools/regulation-check")
async def regulation_check(params: ComplianceRequest = Depends()):
    # This endpoint implements specific logic for frontend display
    result = check_regulation_compliance(params.weight_kg, params.zone, params.altitude_ft, params.purpose)
    
    # Mapper
    status_map = {
        "Compliant": "✅ Compliant",
        "Non-Compliant": "❌ Violation",
        "Conditional": "⚠️ Restricted"
    }
    
    flight_status = status_map.get(result["status"], result["status"])
    
    if params.weight_kg <= 0.25: category = "Nano"
    elif params.weight_kg <= 2.0: category = "Micro"
    elif params.weight_kg <= 25.0: category = "Small"
    else: category = "Medium/Large"

    remarks = result["violations"] + result["required_permits"]
    if not remarks and result["status"] == "Compliant":
        remarks = ["All checks passed."]

    return {
        "flight_status": flight_status,
        "drone_category": category,
        "remarks": remarks
    }

@router.get("/tools/recommend")
async def get_recommendation(params: RecommendRequestSimple = Depends()):
    return mcp_engine.run_tool("recommend_drone", {"max_budget": params.budget, "primary_use": params.use})

@router.get("/tools/find-drones")
async def find_drones(category: str = None, budget: float = None, endurance: int = None, min_flight_time: int = 0, technical_reqs: str = None):
    import pandas as pd
    try:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_path = os.path.join(base_path, "data", "processed", "drone_models.csv")
        
        if not os.path.exists(data_path):
             return {"error": "Data file not found."}

        df = pd.read_csv(data_path)
        if category and category != "All":
            df = df[df['class'].str.lower() == category.lower()]
        if budget:
            df = df[df['price_inr'] <= budget]
        if endurance:
            df = df[df['endurance_min'] >= endurance]
        if min_flight_time:
            df = df[df['endurance_min'] >= min_flight_time]
            
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

@router.get("/tools/download-report")
async def download_report(weight: float, zone: str, alt: float, category: str, status: str):
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Add Logo (if available in project root)
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logo_path = os.path.join(base_path, "logo.png")
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=8, w=30)

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
        
        # Save file temporarily with unique name
        file_path = f"compliance_report_{uuid.uuid4()}.pdf"
        pdf.output(file_path)
        
        # Cleanup task
        def cleanup():
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return FileResponse(file_path, media_type="application/pdf", filename="Drone_Report.pdf", background=BackgroundTask(cleanup))
    except Exception as e:
        print(f"PDF Error: {e}")
        raise HTTPException(status_code=500, detail=f"PDF Generation Failed: {str(e)}")
