import os
import sys
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables
load_dotenv()

# Define absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_DIR = os.path.join(BASE_DIR, "rag", "vector_db")

def setup_database():
    print("🚀 Starting Knowledge Base Construction...")

    documents = []

    # 1. Load Research Summary (Markdown)
    research_path = os.path.join(DOCS_DIR, "research_summary.md")
    if os.path.exists(research_path):
        loader = TextLoader(research_path, encoding='utf-8')
        documents.extend(loader.load())
        print(f"   - Loaded Research Summary")
    else:
        print(f"   ! Warning: {research_path} not found")

    # 2. Load Processed Data (CSVs & JSON)
    # We load JSON as text to avoid complex schema parsing, allowing the LLM to read it raw.
    data_files = ["drone_models.csv", "drone_companies.csv", "training_institutes.csv", "regulations.json"]
    
    for file in data_files:
        file_path = os.path.join(DATA_DIR, file)
        if os.path.exists(file_path):
            if file.endswith(".csv"):
                loader = CSVLoader(file_path, encoding='utf-8')
            else:
                loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
            print(f"   - Loaded {file}")

    # 3. Split Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print(f"   - Split into {len(texts)} chunks")

    # 4. Create Vector Store
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)
        print("   - Cleared existing database")

    print("   - Generating Embeddings and Storing...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=DB_DIR, collection_name="drone_intel")
    print(f"✅ Database successfully populated at {DB_DIR}")

if __name__ == "__main__":
    setup_database()