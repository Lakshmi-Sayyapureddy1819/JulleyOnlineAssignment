import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_read_main():
    """Verify the API is online."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Drone Intelligence API" in response.json()["message"]

def test_calculate_flight():
    """Test the Flight Time Calculator logic."""
    # Params: bat=10Ah, weight=2kg, pay=0.5kg
    response = client.get("/calculate/flight?bat=10&weight=2&pay=0.5")
    assert response.status_code == 200
    data = response.json()
    assert "estimated_minutes" in data
    assert data["estimated_minutes"] > 0

def test_calculate_roi():
    """Test the ROI Calculator logic."""
    response = client.get("/calculate/roi?inv=500000&rev=6000")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Profitable"
    assert data["break_even_days"] > 0

def test_regulation_check():
    """Test the Compliance Tool."""
    response = client.get("/tools/regulation-check?weight_kg=1.5&zone=green&altitude_ft=100")
    assert response.status_code == 200
    data = response.json()
    assert data["flight_status"] == "✅ Compliant"
    assert data["drone_category"] == "Micro"

def test_chat_rag_endpoint():
    """Test the RAG Chatbot (requires OpenAI API Key)."""
    response = client.post("/chat", json={"prompt": "What is a Nano drone?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["sources"], list)