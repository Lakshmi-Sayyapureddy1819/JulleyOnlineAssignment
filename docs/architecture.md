# 🏗️ System Architecture

The Drone Intelligence System follows a modular, three-tier architecture designed for scalability and local performance.

## 1. Frontend (Presentation Tier)
- **Technology**: Streamlit
- **Role**: Provides the interactive dashboard, chat interface, and data visualization (Plotly).
- **Communication**: Communicates with the backend via RESTful HTTP requests.
- **Key Components**:
    - **Chat Interface**: Interactive chat with AI agent.
    - **Tool Panels**: Specialized UI for ROI, Compliance, and Drone Finder.
    - **Smart Recommender**: User-friendly input for drone selection.

## 2. Backend (Logic Tier)
- **Technology**: FastAPI (Asynchronous)
- **Role**: Acts as the orchestrator. It routes user requests to either the RAG Engine or the MCP Calculation tools.
- **Key Services**:
    - **API Router**: Modular endpoints for `/chat` and `/tools`.
    - **Orchestrator**: Manages the flow between user queries and backend services.
    - **MCP Manager**: Central hub for executing specialized Python tools.

## 3. Data & Knowledge (Data Tier)
- **Semantic Storage**: **ChromaDB** (Vector Database) stores embeddings of research PDFs and technical manuals.
- **Structured Storage**: **CSV/JSON** files store drone model specifications and flight logs.
- **Embedding Model**: OpenAI `text-embedding-3-small`.
- **LLM**: OpenAI `gpt-4o-mini`.

## 🔄 Data Flow
1. **Query**: User enters a prompt in the Streamlit UI.
2. **Process**: FastAPI receives the request and the Orchestrator determines intent.
3. **Retrieve/Calculate**: 
    - For policy questions: RAG Engine retrieves context from ChromaDB.
    - For tools: MCP Manager executes the specific calculation mechanism.
4. **Generate**: The LLM generates a natural language response (if needed) or the tool returns raw data.
5. **Display**: Streamlit renders the response and relevant data tables/charts.
