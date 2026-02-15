# Drone Intelligence System for India

A multi-component architecture involving data engineering, a vector database for RAG, an MCP (Model Context Protocol) server for specialized logic, and a FastAPI-driven backend.

## 📂 Repository Structure

```plaintext
drone-intelligence-system/
├── data/                    # Phase 2: Dataset Storage
│   ├── raw/                 # Research docs on Drone Rules 2021 & Indian use cases
│   ├── processed/           # Cleaned CSVs of drone specs & RPTO institutes
│   └── synthetic/           # Generated flight logs & ROI scenario data
├── rag/                     # Phase 3: RAG Components
│   ├── vector_db/           # Persistent ChromaDB/FAISS storage
│   ├── embedder.py          # Embedding generation (OpenAI/HuggingFace)
│   └── retriever.py         # Semantic search & re-ranking logic
├── mcp_server/              # Phase 4: Model Context Protocol Server
│   ├── server.py            # MCP server entry point
│   └── tools/               # Calculation logic
│       ├── flight_calc.py   # Flight time & range estimator
│       ├── roi_calc.py      # Break-even & profitability metrics
│       ├── compliance.py    # Digital Sky zone & permit checker
│       └── assistant.py     # Drone selection logic
├── api/                     # Phase 5: FastAPI Backend
│   ├── main.py              # App entry point & endpoint routing
│   ├── routes/              # /chat, /upload, /calculate endpoints
│   ├── models/              # Pydantic data schemas
│   └── services/            # Glue logic between API, RAG, and MCP
├── frontend/                # Phase 6: Streamlit/React Dashboard
│   ├── public/              # Static assets
│   ├── src/                 # Dashboard components & Chat UI
│   └── .env                 # Frontend configuration
├── tests/                   # Phase 7: Quality Assurance
│   ├── unit/                # Tests for calculators & logic
│   └── integration/         # API & RAG flow testing
├── scripts/                 # Utility Scripts
│   ├── data_gen.py          # Synthetic data generation scripts
│   └── setup_db.py          # Vector database initialization
├── docs/                    # Documentation
│   ├── architecture.png     # System diagrams
│   ├── api_spec.md          # API documentation
│   └── user_guide.md        # Dashboard instructions
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-container orchestration
├── requirements.txt         # Python dependencies
└── README.md                # Setup & submission details
```

## 🛠️ Key Implementation Components
- **Data Ingestion**: Scripts to turn raw PDFs into searchable vectors.
- **Tool Intelligence**: MCP server acting as the "calculator brain".
- **API Gateway**: Orchestrator for RAG and MCP logic.