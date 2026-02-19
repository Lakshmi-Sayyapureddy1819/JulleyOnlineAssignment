import sys
import os
from fastapi import FastAPI, UploadFile, File
from api.routes import chat, tools
from rag.retriever import ingest_multimodal_data

# Add the project root to the python path to allow imports from sibling directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="India Drone Intel API")

# Register modular routes
app.include_router(chat.router, tags=["AI Chat"])
app.include_router(tools.router, tags=["Drone Tools"])

@app.get("/")
async def root():
    return {"message": "Welcome to the India Drone Intelligence API"}

@app.get("/analytics")
async def analytics():
    return {"status": "System Operational", "active_modules": ["RAG", "Flight Calc", "ROI Calc", "Compliance", "Recommendation"]}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Save file temporarily to handle it as a path for multi-modal ingestion
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        chunks = ingest_multimodal_data(temp_filename, file.content_type)
        return {"message": "Document processed successfully", "chunks_added": chunks}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)