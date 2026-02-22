# Revisia - AI-Powered History Tutor

An educational AI chatbot for Grade 10 and 11 History students, powered by RAG (Retrieval-Augmented Generation) and Google Gemini.

## Features

- 📚 RAG-based question answering using Grade 10 & 11 History textbooks
- 💬 Chat interface with conversation history
- 🔐 User authentication and personalized chat sessions
- 📖 Page references in answers
- 🔄 **Multiple vector store support** - Switch between different content sources
- 🗄️ MongoDB for user and chat storage

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# MongoDB Configuration
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=revisia

# Security
SECRET_KEY=your_secret_key_here

# Google Gemini API
GOOGLE_API_KEY=your_google_api_key

Debug Mode
DEBUG=True
```

### 3. Place Your Pre-built Vector Store(s)

This application requires pre-built FAISS vector stores. You can have multiple vector stores for different content.

1. **Create the vectorstore folder:**
   ```
   mkdir vectorstore
   ```

2. **Add your vector stores:**
   Place your vector store folders inside `vectorstore/`:
   ```
   vectorstore/
   ├── G10_G11_history_vector_store/      # English medium (default)
   │   ├── index.faiss
   │   └── index.pkl
   ├── G10_G11_history_sinhala_vector_store/  # Sinhala medium
   │   ├── index.faiss
   │   └── index.pkl
   └── G10_G11_history_tamil_vector_store/    # Tamil medium
       ├── index.faiss
       └── index.pkl
   ```

3. **Configure vector stores in `src/config.py`:**
   Edit the `VECTOR_STORES` dictionary to add or modify vector store configurations:
   ```python
   VECTOR_STORES = {
       "grade_10_11": {
           "path": "vectorstore/G10_G11_history_vector_store",
           "description": "Grade 10 and 11 History (English Medium)",
           "grades": [10, 11]
       },
       "sinhala_medium": {
           "path": "vectorstore/G10_G11_history_sinhala_vector_store",
           "description": "Grade 10 and 11 History (Sinhala Medium)",
           "grades": [10, 11]
       },
       # Add more as needed
   }
   ```

### 4. Run the Application

```bash
streamlit run src/main.py
```

## Using Multiple Vector Stores

The application now supports switching between different vector stores during chat sessions. This is useful for:

- **Different languages** (English, Sinhala, Tamil medium textbooks)
- **Different grades** (Grade 10 only, Grade 11 only, or combined)
- **Different subjects** (if you expand beyond History)

### How to Switch Vector Stores:

1. In the sidebar, look for the **"Content Selection"** dropdown
2. Select your desired content source
3. Continue chatting - responses will use the selected vector store

### Adding New Vector Stores:

1. **Build the vector store** using the Kaggle notebook (`revisiatest02.ipynb`)
2. **Download** the generated `index.faiss` and `index.pkl` files
3. **Place them** in a new folder under `vectorstore/`
4. **Update** `src/config.py` to add the new configuration:
   ```python
   "your_new_store": {
       "path": "vectorstore/your_new_store_folder",
       "description": "Description shown in UI",
       "grades": [10, 11]  # or relevant grades
   }
   ```
5. **Restart** the application

## Project Structure

```
revisia/
├── src/
│   ├── main.py              # Streamlit app entry point
│   ├── auth.py              # Authentication UI and logic
│   ├── chat.py              # Chat interface with vector store selection
│   ├── config.py            # Configuration with VECTOR_STORES mapping
│   ├── styles.py            # Custom CSS styles
│   ├── database/
│   │   ├── mongodb.py       # MongoDB operations
│   │   └── models.py        # Data models
│   ├── rag/
│   │   ├── embeddings.py    # Embedding model management
│   │   ├── pdf_processor.py # Vector store loading
│   │   └── retriever.py     # RAG retrieval and generation
│   └── utils/
│       └── helpers.py       # Utility functions
├── vectorstore/             # Pre-built FAISS vector stores (required)
│   ├── G10_G11_history_vector_store/
│   │   ├── index.faiss
│   │   └── index.pkl
│   └── ... (add more vector stores as needed)
├── revisiatest02.ipynb      # Kaggle notebook for building vector stores
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration Reference

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_VECTOR_STORE` | Key for default vector store | `grade_10_11` |
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `MONGODB_URI` | MongoDB connection string | Required |
| `DATABASE_NAME` | MongoDB database name | `revisia` |

### Vector Store Configuration

Edit `src/config.py` to manage your vector stores:

```python
VECTOR_STORES = {
    "key_name": {
        "path": "vectorstore/folder_name",
        "description": "User-friendly description",
        "grades": [10, 11]  # Optional metadata
    }
}
```

## How It Works

1. **Vector Store Loading**: The application loads a pre-built FAISS vector store based on user selection
2. **User Query**: When a user asks a question:
   - The question is embedded using Google's gemini-embedding-001 model
   - Similar chunks are retrieved from the selected vector store
   - Context is extracted with page numbers and grades
   - Google Gemini generates a focused answer using the context
3. **Chat History**: All conversations are stored in MongoDB per user
4. **Dynamic Switching**: Users can switch between vector stores mid-conversation

## API Usage Example

```python
from rag.retriever import generate_response

# Use default vector store
answer = generate_response("What is numismatics?")

# Use specific vector store
answer = generate_response(
    "What is numismatics?",
    vector_store_key="sinhala_medium"
)
```

## Troubleshooting

### Vector store not found
Ensure your vector store folder exists at the path specified in `Config.VECTOR_STORES` and contains both `index.faiss` and `index.pkl` files.

### API Key errors
Make sure your `.env` file has a valid `GOOGLE_API_KEY`.

### Vector store selection not appearing
Check that you have multiple vector stores configured in `src/config.py` and the folders exist.

## Credits

- **LangChain**: Document processing and RAG framework
- **FAISS**: Vector similarity search
- **Google Gemini**: LLM for answer generation
- **Streamlit**: Web interface
- **MongoDB**: Data persistence