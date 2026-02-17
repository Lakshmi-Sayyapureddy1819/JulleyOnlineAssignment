# 🛸 Drone Intelligence System for India

An advanced AI-driven platform for analyzing drone regulations, calculating business ROI, and simulating flight telemetry within the Indian ecosystem. This project was developed as part of the JulleyOnline AI/ML Internship.

## 🌟 Key Features
* **Agentic RAG System**: Query Drone Rules 2021 and industry datasets using OpenAI-powered semantic search.
* **MCP Calculation Tools**: Deterministic calculators for flight endurance and ROI analysis.
* **Synthetic Data Engine**: Generates 1,000+ flight logs for compliance and analytics testing.
* **Interactive Dashboard**: A Streamlit interface featuring a real-time chatbot and data visualizations.

---

## 🏗️ Project Structure
```text
drone-intelligence-system/
├── api/                  # FastAPI Backend & Endpoints
├── data/                 # Raw, Processed, and Synthetic Datasets
├── docs/                 # Documentation & Architecture Diagrams
├── frontend/             # Streamlit Dashboard Source
├── mcp_server/           # Model Context Protocol (Calculators)
├── rag/                  # Vector Database & Retriever Logic
├── scripts/              # Data Generation & DB Setup Scripts
└── requirements.txt      # Project Dependencies
```

## 🚀 Quick Start Guide

### 1. Environment Setup
Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_actual_key_here
```

### 3. Data & Database Initialization
Generate the synthetic datasets and initialize the ChromaDB vector store:

```bash
python scripts/data_generation.py
python scripts/database_setup.py
```

### 4. Launch the Application
Run the backend and frontend in separate terminals:

**Backend:** `uvicorn api.main:app --reload`

**Frontend:** `streamlit run frontend/src/app.py`

## 🛠️ Tech Stack
* **Language**: Python 3.12
* **AI Framework**: LangChain, OpenAI GPT-4o Mini
* **Vector DB**: ChromaDB
* **API Layer**: FastAPI
* **Visualization**: Plotly, Streamlit