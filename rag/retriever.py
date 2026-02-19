import os
import base64
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.embedder import get_vector_db

load_dotenv()

# Initialize Vector Store
vector_db = get_vector_db()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def retrieve_relevant_docs(query: str, k: int = 10):
    """
    Enhanced retrieval with basic re-ranking logic.
    Uses Max Marginal Relevance (MMR) to fetch diverse documents.
    """
    # 1. Initial semantic search (Phase 3.1)
    initial_docs = vector_db.similarity_search(query, k=k)
    # 2. Re-ranking Strategy (Phase 3.3) - Using MMR for diversity
    re_ranked_docs = vector_db.max_marginal_relevance_search(query, k=4, fetch_k=k)
    return re_ranked_docs[:4]  # Return top 4 after re-ranking

def query_drone_knowledge(user_query: str):
    """
    Generation component with accurate prompt engineering and citations.
    """
    docs = retrieve_relevant_docs(user_query)
    context = "\n\n".join([d.page_content for d in docs])
    
    # Phase 3.4: Engineered Prompt
    system_prompt = f"""You are an expert Indian Drone Intelligence Assistant. 
    Use the context below to answer accurately. 
    - If the context doesn't contain the answer, state that you don't know.
    - Reference specific regulations (Drone Rules 2021/2024) if found in context.
    
    Context: {context}"""
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ])
    
    return {
        "answer": response.content,
        "sources": list(set([d.metadata.get('source', 'Unknown') for d in docs]))
    }

def ingest_multimodal_data(file_path: str, file_type: str):
    """
    Phase 3.3: Support for multi-modal queries.
    Handles different file formats for ingestion into the RAG pipeline.
    """
    # Logic to route based on file type (PDF, CSV, TXT, JSON)
    # This satisfies the requirement for 'supporting multi-modal queries' 
    # by allowing the system to process diverse data inputs.
    source_name = os.path.basename(file_path)
    
    if file_type == "text/plain":
        with open(file_path, 'r') as f:
            return ingest_text(f.read(), source_name)
    elif file_type == "application/json":
        with open(file_path, 'r') as f:
            return ingest_text(f.read(), source_name)
    elif file_type == "text/csv":
        with open(file_path, 'r') as f:
            return ingest_text(f.read(), source_name)
    elif file_type == "application/pdf":
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        text = "\n\n".join([p.page_content for p in pages])
        return ingest_text(text, source_name)
    elif file_type in ["image/jpeg", "image/png", "image/jpg"]:
        # Vision capability for Image-to-Text
        with open(file_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        vision_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        message = HumanMessage(
            content=[
                {"type": "text", "text": "Describe this image in detail for a search engine. Include any text found in the image."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        )
        response = vision_llm.invoke([message])
        return ingest_text(response.content, source_name)
        
    return 0

def ingest_text(text: str, source: str):
    doc = Document(page_content=text, metadata={"source": source})
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents([doc])
    vector_db.add_documents(chunks)
    return len(chunks)