from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config.settings import settings
import chromadb
import os

def get_vector_store():
    """Initializes and returns the ChromaDB connection."""
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY must be set to initialize Embeddings.")
        
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", 
        api_key=settings.OPENAI_API_KEY
    )
    
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    persistent_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    
    vector_store = Chroma(
        client=persistent_client,
        collection_name="freelance_jobs",
        embedding_function=embeddings,
    )
    
    return vector_store
