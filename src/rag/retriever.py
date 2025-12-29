from langchain_community.vectorstores import FAISS
from google import genai
from config import Config
from rag.pdf_processor import load_vector_store
import os

def retrieve_relevant_info(query, db):
    # Function to retrieve relevant information from the MongoDB database based on user queries
    results = db.chat_history.find({"$text": {"$search": query}})
    return list(results)

def get_user_chats(user_id, db):
    # Function to get chat history for a specific user
    user_chats = db.chat_history.find({"user_id": user_id})
    return list(user_chats)

def retrieve_user_info(user_id, db):
    # Function to retrieve user information from the database
    user_info = db.users.find_one({"_id": user_id})
    return user_info

def chat_gemini(question: str, context: str = None, model: str = None):
    """
    RAG-based History assistant for Grade 10 & 11 students
    with page references
    """
    if model is None:
        model = Config.LLM_MODEL
    
    prompt_text = """
        You are an educational AI tutor specialized in Grade 10 and Grade 11 History.
        
        INSTRUCTIONS:
        - Answer ONLY questions related to Grade 10 or Grade 11 History.
        - Use ONLY the provided context to answer.
        - Cite page numbers from the context in your answer.
        - Do NOT guess or add information not present in the context.
        - If the answer is not found in the context, say:
          "The provided material does not contain enough information to answer this question."
        - Use clear, student-friendly language.
        - Keep the answer concise and exam-oriented.
        - Do NOT express opinions or modern interpretations.
        - Do NOT mention that you are an AI.
        
        TONE:
        - Neutral
        - Educational
        - Clear
        
        OUTPUT FORMAT (STRICT):
        - Main answer in short paragraphs or bullet points
        - End with a separate line:
          References: Page X, Page Y
        
        Keep the total answer under 150 words.
        """
    
    if context:
        prompt_text += f"\n\nCONTEXT:\n{context}\n"
    
    prompt_text += f"""
        QUESTION:
        {question}
        
        ANSWER:
        """
    
    client = genai.Client(api_key=Config.GOOGLE_API_KEY)
    
    response = client.models.generate_content(
        model=model,
        contents=prompt_text
    )
    
    return response.text

def generate_response(question: str, k: int = 3, vector_store_key: str = None):
    """
    Generate a RAG response for the given question
    
    Args:
        question: User's question
        k: Number of similar documents to retrieve
        vector_store_key: Which vector store to use (e.g., 'grade_10_11', 'sinhala_medium')
                         If None, uses the default from config
    
    Returns:
        Generated answer with references
    """
    try:
        # Load vector store
        vectorstore = load_vector_store(vector_store_key)
        
        # Retrieve relevant documents
        docs = vectorstore.similarity_search(question, k=k)
        
        if not docs:
            return "I couldn't find relevant information in the textbooks. Please try rephrasing your question."
        
        # Combine context from retrieved documents
        context_parts = []
        for doc in docs:
            page_num = doc.metadata.get('page', 'Unknown')
            grade = doc.metadata.get('grade', 'Unknown')
            context_parts.append(
                f"[Grade {grade}, Page {page_num}]\n{doc.page_content}"
            )
        
        context = "\n\n".join(context_parts)
        
        # Generate answer using Gemini
        answer = chat_gemini(question, context=context)
        
        return answer
    except FileNotFoundError as e:
        return (f"⚠️ {str(e)}\n\n"
                "Please ensure your vector store is placed in the correct location.")
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}\n\nPlease contact support if this persists."

def generate_dummy_response(user_input: str, vector_store_key: str = None):
    """
    Wrapper for backward compatibility - uses actual RAG now
    
    Args:
        user_input: User's question
        vector_store_key: Which vector store to use (optional)
    """
    return generate_response(user_input, vector_store_key=vector_store_key)
