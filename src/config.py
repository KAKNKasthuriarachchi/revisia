import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv("MONGODB_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vectorstore/G10_G11_history_vector_store")

    VECTOR_STORES = {
        "grade_10_11": {
            "path": "vectorstore/G10_G11_history_vector_store",
            "description": "Grade 10 and 11 History (English Medium)",
            "grades": [10, 11]
        },
    }
    
    DEFAULT_VECTOR_STORE = os.getenv("DEFAULT_VECTOR_STORE", "grade_10_11")
    
    EMBEDDING_MODEL = "models/text-embedding-004"
    LLM_MODEL = "gemini-2.0-flash-exp"
    
    @classmethod
    def get_vector_store_path(cls, store_key: str = None) -> str:
        """
        Get the path for a specific vector store
        
        Args:
            store_key: Key from VECTOR_STORES dict (e.g., 'grade_10_11')
                      If None, uses DEFAULT_VECTOR_STORE
        
        Returns:
            Path to the vector store
        """
        if store_key is None:
            store_key = cls.DEFAULT_VECTOR_STORE
        
        if store_key in cls.VECTOR_STORES:
            return cls.VECTOR_STORES[store_key]["path"]
        else:
            # Fallback to default path
            return cls.VECTOR_STORE_PATH
    
    @classmethod
    def get_vector_store_info(cls, store_key: str = None) -> dict:
        """
        Get full information about a vector store
        
        Args:
            store_key: Key from VECTOR_STORES dict
        
        Returns:
            Dictionary with path, description, and grades
        """
        if store_key is None:
            store_key = cls.DEFAULT_VECTOR_STORE
        
        return cls.VECTOR_STORES.get(store_key, {
            "path": cls.VECTOR_STORE_PATH,
            "description": "Default Vector Store",
            "grades": [10, 11]
        })
    
    @classmethod
    def list_available_vector_stores(cls) -> list:
        """
        Get list of all available vector store configurations
        
        Returns:
            List of tuples (key, description)
        """
        return [(key, info["description"]) for key, info in cls.VECTOR_STORES.items()]