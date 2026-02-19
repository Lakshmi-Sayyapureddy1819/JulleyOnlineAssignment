# 📖 API Specification

The Drone Intelligence System backend is built with FastAPI and serves as the bridge between the RAG knowledge base and specialized MCP tools.

## 🤖 AI & RAG Endpoints

### Chat Assistant
- **Endpoint**: `POST /chat`
- **Payload**: `{"prompt": "string"}`
- **Description**: Processes natural language queries about drone regulations and business logic.
- **Response**: Returns an answer with specific document citations.

### Document Ingestion
- **Endpoint**: `POST /upload`
- **Payload**: Form-data (File)
- **Description**: Uploads a text file to be chunked and added to the ChromaDB vector store.

## 🛠️ MCP Tool Endpoints

### Regulation Compliance Checker
- **Endpoint**: `GET /tools/regulation-check`
- **Params**: `weight_kg`, `zone`, `altitude_ft`, `purpose`
- **Description**: Validates flight safety against Indian Drone Rules 2021. Returns friendly status messages and remarks.

- **Endpoint**: `GET /check/compliance`
- **Params**: `weight_kg`, `zone`, `altitude_ft`, `purpose`
- **Description**: Core compliance check returning raw status and violations.

### ROI Calculator
- **Endpoint**: `GET /calculate/roi`
- **Params**: `inv` (Investment), `rev` (Daily Revenue), `op_costs` (Optional), `use_case` (Optional)
- **Description**: Calculates break-even timeline and net profitability.

### Flight Endurance Estimator
- **Endpoint**: `GET /calculate/flight`
- **Params**: `bat` (Ah), `weight` (kg), `pay` (kg), `wind` (Optional)
- **Description**: Provides estimated and safe flight durations.

### Drone Finder
- **Endpoint**: `GET /tools/find-drones`
- **Params**: `category`, `budget`, `endurance`, `min_flight_time`, `technical_reqs`
- **Description**: Queries the processed CSV database for specific drone models.

### Smart Recommendation
- **Endpoint**: `GET /tools/recommend`
- **Params**: `budget`, `use`
- **Description**: AI-driven recommendation logic based on budget and use case.

### Report Generation
- **Endpoint**: `GET /tools/download-report`
- **Params**: `weight`, `zone`, `alt`, `category`, `status`
- **Description**: Generates a PDF compliance report.

## 📊 System Endpoints
- **Endpoint**: `GET /analytics`
- **Description**: Returns system health status and active service modules.