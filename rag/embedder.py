import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

def get_vector_db():
    """
    Initializes and returns the Chroma vector database using OpenAI embeddings.
    """
    # Define absolute path for the database to avoid path issues
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_DIR = os.path.join(BASE_DIR, "rag", "vector_db")
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
        collection_name="drone_intel"
    )