from google import genai
from config import Config, FallbackResponse, Grade, Language
from rag.pdf_processor import load_vector_store
from pathlib import Path

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

def load_prompt_template(name: str) -> str:
    """Load a prompt template from disk, or return the provided default."""
    # Get absolute path to prompts directory
    prompts_dir = Path(__file__).resolve().parent.parent / "prompts"
    template_path = prompts_dir / name
    
    try:
        return template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Template '{name}' not found at {template_path}")

def chat_gemini(
        question: str,
        rewritten_query: str, 
        context: str = None, 
        model: str = None,
        template_name: str = "history_tutor_default.txt"):
    """
    RAG-based History assistant for Grade 10 & 11 students
    with page references
    """
    model = Config.LLM_MODEL
    
    # load external template if present
    prompt_text = load_prompt_template(template_name)

    # Add context and question to the prompt
    if context:
        prompt_text += f"\n\nCONTEXT:\n{context}\n"
    else:
        return FallbackResponse.NO_CONTEXT.value
    if rewritten_query:
        prompt_text += f"\n\nINTERPRETED QUESTION:\n{rewritten_query}\n"

    prompt_text += f"\n\nQUESTION:\n{question}\n\nANSWER:\n"
    
    client = genai.Client(api_key=Config.GOOGLE_API_KEY)
    # print("Prompt sent to Gemini:", prompt_text)
    response = client.models.generate_content(
        model=model,
        contents=prompt_text
    )
    
    return response.text

def generate_response(
    question: str, 
    grade: Grade = Grade.O_LEVEL,
    language: Language = Language.ENGLISH,
    chat_history: list = None,
    k: int = 5
) -> str:
    """
    Generate a RAG response for the given question
    
    Args:
        question: User's question
        grade: Grade
        language: Language (ENGLISH, SINHALA, or TAMIL)
        k: Number of similar documents to retrieve
    
    Returns:
        Generated answer with references
    """
    history_text = ""
    additional_context = ""

    if chat_history:
        recent_history = chat_history[-6:-1]  # last 6 messages

        for msg in recent_history:
            role = msg["role"]
            content = msg["message"]

            additional_context += f"{content}."
            history_text += f"{role}: {content}\n"

    rewritten_query = rewrite_query(question, chat_history)

    try:
        # Get the appropriate vector store key based on grade and language
        vector_store_key = Config.get_vector_store_key(grade, language)
        
        # Load vector store
        vectorstore = load_vector_store(vector_store_key)
        
        # Retrieve relevant documents
        docs = vectorstore.similarity_search(rewritten_query, k=5)
        # print(f"Retrieved {docs} documents from vector store '{vector_store_key}' for query: '{rewritten_query}'")
        if not docs:
            return FallbackResponse.NO_CONTEXT
        
        # Combine context from retrieved documents
        context_parts = []
        for doc in docs:
            page_num = doc.metadata.get('page', 'Unknown')
            grade_meta = doc.metadata.get('grade', 'Unknown')
            context_parts.append(
                f"[Grade {grade_meta}, Page {page_num}]\n{doc.page_content}"
            )
        
        context = "\n\n".join(context_parts)
        
        # Select template based on language
        template_map = {
            Language.ENGLISH: "history_tutor_default.txt",
            Language.SINHALA: "history_tutor_si.txt",
            Language.TAMIL: "history_tutor_ta.txt"
        }
        template_name = template_map.get(language, "history_tutor_default.txt")
        
        # Generate answer using Gemini
        # print("Question:", rewritten_query)
        answer = chat_gemini(question, rewritten_query, context=context, template_name=template_name)
        return answer
    except FileNotFoundError as e:
        return f"{str(e)}\n\n{FallbackResponse.VECTOR_STORE_NOT_FOUND.value}"
    except Exception as e:
        return f"{FallbackResponse.GENERIC_ERROR.value}\n\nError: {str(e)}"
    
def rewrite_query(question, chat_history):
    if not chat_history or len(chat_history) < 2:
        # print("No chat history, using original question.")
        return question
    history_text = ""

    for msg in chat_history:
        role = msg["role"]
        content = msg["message"]

        history_text += f"{role}: {content}\n"

    client = genai.Client(api_key=Config.GOOGLE_API_KEY)
    rewrite_prompt = load_prompt_template("rewrite_agent.txt").format(
        history_text=history_text,
        question=question
    )
    response = client.models.generate_content(
        model=Config.QUERY_REWRITE_MODEL,
        contents=rewrite_prompt
    )

    return response.text.strip()