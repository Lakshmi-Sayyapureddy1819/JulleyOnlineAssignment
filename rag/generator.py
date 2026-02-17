from langchain_openai import ChatOpenAI
from rag.retriever import retrieve_relevant_docs
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM (GPT-4o mini is cost-effective and fast)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def generate_drone_response(user_query: str):
    """
    Orchestrates the RAG process: Retrieval -> Context Assembly -> Generation
    """
    # 1. Retrieve top context chunks from the vector DB
    context_docs = retrieve_relevant_docs(user_query)
    context_text = "\n\n".join([doc.page_content for doc in context_docs])
    
    # 2. Extract unique source names for citations
    sources = list(set([doc.metadata.get('source', 'Unknown Document') for doc in context_docs]))
    
    # 3. Construct the System Prompt
    system_prompt = f"""
    You are an expert Indian Drone Intelligence Assistant. 
    Use the following pieces of context to answer the user's question accurately.
    
    - If the answer is not in the context, say: "I am sorry, but my current knowledge base doesn't contain that specific detail."
    - Refer to specific Drone Rules 2021 or 2024 updates if mentioned in the context.
    - Always maintain a professional and helpful tone.

    Context:
    {context_text}
    """
    
    # 4. Get response from LLM
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ])
    
    return {
        "answer": response.content,
        "citations": sources
    }