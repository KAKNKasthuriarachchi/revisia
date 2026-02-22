from langchain_community.vectorstores import FAISS
from rag.embeddings import load_model
from config import Config
import os


def load_vector_store(vector_store_key: str = None):
    """
    Load an existing FAISS vector store
    
    Args:
        vector_store_key: Key from Config.VECTOR_STORES dict to specify which vector store to load    
    Returns:
        FAISS vectorstore object
    """
    # Get the path for the specified vector store
    vector_store_path = Config.get_vector_store_path(vector_store_key)
    
    if not os.path.exists(vector_store_path):
        available_stores = Config.list_available_vector_stores()
        store_list = "\n".join([f"  - {key}: {desc}" for key, desc in available_stores])
        raise FileNotFoundError(
            f"Vector store not found at {vector_store_path}.\n"
            f"Available vector store configurations:\n{store_list}\n\n"
            f"Please ensure the vector store exists before running the application."
        )
    
    embeddings = load_model()
    vectorstore = FAISS.load_local(
        vector_store_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    
    return vectorstore
