import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.embedder import get_vector_db

load_dotenv()

# Initialize Vector Store using the shared embedder module
vector_db = get_vector_db()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def retrieve_relevant_docs(query: str, k: int = 4):
    """
    Retrieves relevant documents from the vector database.
    """
    return vector_db.similarity_search(query, k=k)

def query_drone_knowledge(user_query: str):
    # Retrieve top 4 relevant documents from all datasets
    docs = retrieve_relevant_docs(user_query)
    context = "\n\n".join([d.page_content for d in docs])
    
    prompt = f"""You are an Indian Drone Intelligence Assistant. 
    Use the context below to answer accurately. 
    Context: {context}
    
    Question: {user_query}
    
    Answer (Include sources if available):"""
    
    response = llm.invoke(prompt)
    return {
        "answer": response.content,
        "sources": list(set([d.metadata.get('source') for d in docs]))
    }

def ingest_text(text: str, source: str):
    doc = Document(page_content=text, metadata={"source": source})
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents([doc])
    vector_db.add_documents(chunks)
    return len(chunks)