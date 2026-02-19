import os
import sys
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, CSVLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables
load_dotenv()

# Define absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "rag", "vector_db")

def setup_database():
    print("🚀 Starting Knowledge Base Construction...")

    documents = []
    
    # Define folders to traverse
    folders = {
        "raw": os.path.join(BASE_DIR, "data", "raw"),
        "processed": os.path.join(BASE_DIR, "data", "processed"),
        "synthetic": os.path.join(BASE_DIR, "data", "synthetic"),
        "docs": os.path.join(BASE_DIR, "docs")
    }

    for folder_name, path in folders.items():
        if not os.path.exists(path):
            print(f"   ! Warning: Folder {path} not found")
            continue
            
        print(f"   - Scanning {folder_name} folder...")
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            try:
                if file.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                    print(f"     + Loaded PDF: {file}")
                elif file.endswith(".csv"):
                    loader = CSVLoader(file_path, encoding='utf-8')
                    documents.extend(loader.load())
                    print(f"     + Loaded CSV: {file}")
                elif file.endswith(".json") or file.endswith(".txt") or file.endswith(".md"):
                    loader = TextLoader(file_path, encoding='utf-8')
                    documents.extend(loader.load())
                    print(f"     + Loaded Text/JSON: {file}")
            except Exception as e:
                print(f"     ! Error loading {file}: {e}")

    # 3. Split Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print(f"   - Split into {len(texts)} chunks")

    # 4. Create Vector Store
    if os.path.exists(DB_DIR):
        try:
            shutil.rmtree(DB_DIR)
            print("   - Cleared existing database")
        except PermissionError:
            print("   ! Error: Could not clear existing database. Is the backend server running?")
            print("   ! Please stop 'python api/main.py' and try again.")
            return

    print("   - Generating Embeddings and Storing...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=DB_DIR, collection_name="drone_intel")
    print(f"✅ Database successfully populated at {DB_DIR}")

if __name__ == "__main__":
    setup_database()