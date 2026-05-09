import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class Language(Enum):
    """Supported languages"""
    ENGLISH = {
        "key":"en",
        "label":"English"
        }
    SINHALA = {
        "key":"si",
        "label":"Sinhala"}
    TAMIL = {
        "key":"ta",
        "label":"Tamil"
    }
    
    @property
    def key(self):
        """Get the language key (e.g., 'en', 'si', 'ta')"""
        return self.value["key"]
    
    @property
    def label(self):
        """Get the language label (e.g., 'English', 'Sinhala', 'Tamil')"""
        return self.value["label"]

class Grade(Enum):
    """Supported grade levels"""
    GRADE_6 = {
        "key": "grade_6",
        "label": "Grade 6"
    }
    GRADE_7 = {
        "key": "grade_7",
        "label": "Grade 7"
    }
    GRADE_8 = {
        "key": "grade_8",
        "label": "Grade 8"
    }
    GRADE_9 = {
        "key": "grade_9",
        "label": "Grade 9"
    }
    O_LEVEL = {
        "key": "o_level",
        "label": "O/L"
    }
    
    @property
    def key(self):
        """Get the grade key (e.g., 'grade_6', 'o_level')"""
        return self.value["key"]
    
    @property
    def label(self):
        """Get the grade label (e.g., 'Grade 6', 'O/L')"""
        return self.value["label"]
    

class FallbackResponse(Enum):
    """Enum for fallback response messages"""
    NO_CONTEXT = "Sorry, I couldn't find any relevant information to answer your question. Please try asking in a different way or provide more details."
    GREETINGS = {
        "en": "Hello! I'm your History tutor. Select your grade and language from the sidebar to get started.",
        'si': "ආයුබෝවන්! මම ඔබගේ ඉතිහාස ගුරුවරයා වෙමි. පළමුව ඔබගේ ශ්‍රේණිය සහ භාෂාව තෝරන්න.",
        'ta': "வணக்கம்! நான் உங்கள் வரலாறு ஆசிரியர். முதலில் உங்கள் தரம் மற்றும் மொழியை தேர்ந்தெடுக்கவும்.",
    }
    VECTOR_STORE_NOT_FOUND = "Vector store not found. Please ensure the textbooks are properly indexed."
    GENERIC_ERROR = "Sorry, I encountered an error. Please try again or contact support if this persists."
    
    @classmethod
    def get(cls, key: str, default: str = None) -> str:
        """Get response by name or return default"""
        try:
            return cls[key.upper()].value
        except KeyError:
            return default or f"[Missing response: {key}]"

class Config:
    MONGODB_URI = os.getenv("DATABASE_URL")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    EMBEDDING_MODEL = "models/gemini-embedding-001"
    LLM_MODEL ="models/gemini-2.5-flash-lite"
    VECTOR_STORES = {
        f"{Grade.O_LEVEL.key}_{Language.ENGLISH.key}": {
            "path": "vectorstore/OL_E_history_vector_store",
            "description": "Grade 10 and 11 History (English Medium)",
            "grades": [10, 11]
            
        },
        f"{Grade.O_LEVEL.key}_{Language.SINHALA.key}": {
            "path": "vectorstore/OL_S_history_vector_store",
            "description": "Grade 10 and 11 History (Sinhala Medium)",
            "grades": [10, 11]
        },
        f"{Grade.O_LEVEL.key}_{Language.TAMIL.key}": {
            "path": "vectorstore/OL_T_history_vector_store",
            "description": "Grade 10 and 11 History (Tamil Medium)",
            "grades": [10, 11]
        }, 
         f"{Grade.GRADE_6.key}_{Language.ENGLISH.key}": {
            "path": "vectorstore/G06_E_history_vector_store",
            "description": "Grade 6 History (English Medium)",
            "grades": [6]
            
        },
        f"{Grade.GRADE_6.key}_{Language.SINHALA.key}": {
            "path": "vectorstore/G06_S_history_vector_store",
            "description": "Grade 6 History (Sinhala Medium)",
            "grades": [6]
            
        }, 
         f"{Grade.GRADE_7.key}_{Language.ENGLISH.key}": {
            "path": "vectorstore/G07_E_history_vector_store",
            "description": "Grade 7 History (English Medium)",
            "grades": [7]
            
        },   
         f"{Grade.GRADE_7.key}_{Language.SINHALA.key}": {
            "path": "vectorstore/G07_S_history_vector_store",
            "description": "Grade 7 History (Sinhala Medium)",
            "grades": [7]
            
        }, 
          f"{Grade.GRADE_8.key}_{Language.ENGLISH.key}": {
            "path": "vectorstore/G08_E_history_vector_store",
            "description": "Grade 8 History (English Medium)",
            "grades": [8]
            
        },
          f"{Grade.GRADE_8.key}_{Language.SINHALA.key}": {
            "path": "vectorstore/G08_S_history_vector_store",
            "description": "Grade 8 History (Sinhala Medium)",
            "grades": [8]
            
        },
            f"{Grade.GRADE_9.key}_{Language.ENGLISH.key}": {
            "path": "vectorstore/G09_E_history_vector_store",
            "description": "Grade 9 History (English Medium)",
            "grades": [9]
            
        },
    }
    DEFAULT_VECTOR_STORE = VECTOR_STORES.get('grade_OL_E')
    
    
    @classmethod
    def get_vector_store_key(cls, grade: Grade, language: Language) -> str:
        """
        Get the vector store key based on grade and language
        
        Args:
            grade: Grade enum (A_LEVEL or O_LEVEL)
            language: Language enum (ENGLISH, SINHALA, or TAMIL)
            
        Returns:
            Vector store key string
        """
        # Convert enums to values if they aren't already
        grade_val = grade.key if isinstance(grade, Grade) else grade
        lang_val = language.key if isinstance(language, Language) else language
        
        key = f"{grade_val}_{lang_val}"
        
        if key not in cls.VECTOR_STORES:
            raise ValueError(f"No vector store found for grade '{grade_val}' and language '{lang_val}'")
        
        return key
    
    @classmethod
    def get_vector_store_path(cls, store_key: str = None, grade: Grade = None, language: Language = None) -> str:
        """
        Get the path for a specific vector store
        
        Args:
            store_key: Key from VECTOR_STORES dict (e.g., 'grade_10_11')        
        Returns:
            Path to the vector store
        """
        if store_key is None:
            if grade is None or language is None:
                raise ValueError("Either store_key or both grade and language must be provided")
            store_key = cls.get_vector_store_key(grade, language)
        
        if store_key in cls.VECTOR_STORES:
            return cls.VECTOR_STORES[store_key]["path"]
        else:
            raise ValueError(f"Vector store key '{store_key}' not found in configuration.")
        
    @classmethod
    def get_default_vector_store(cls) -> str:
        """Get the default vector store key"""
        return list(cls.VECTOR_STORES.keys())[0]
    
    @classmethod
    def list_available_vector_stores(cls) -> list:
        """List all available vector stores with their descriptions"""
        return [(key, store["description"]) for key, store in cls.VECTOR_STORES.items()]
    
    @classmethod
    def get_vector_store_info(cls, store_key: str) -> dict:
        """Get information about a specific vector store"""
        return cls.VECTOR_STORES.get(store_key, {})

