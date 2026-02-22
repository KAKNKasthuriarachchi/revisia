from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import Config

_embedding_model = None

def load_model():
    """Load Google Generative AI embeddings model"""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = GoogleGenerativeAIEmbeddings(
            model=Config.EMBEDDING_MODEL,
            google_api_key=Config.GOOGLE_API_KEY
        )
    return _embedding_model

def get_embeddings(text):
    """Generate embeddings for the provided text"""
    model = load_model()
    return model.embed_query(text)