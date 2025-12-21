# Revisia - RAG Chat Application

## Overview
Revisia is a Retrieval-Augmented Generation (RAG) chat application built using Streamlit and MongoDB. It allows users to engage in conversations while leveraging a database to retrieve relevant information and maintain chat history.

## Project Structure
```
revisia
├── src
│   ├── main.py                # Entry point of the application
│   ├── auth.py                # User authentication UI
│   ├── chat.py                # Chat interface management
│   ├── styles.py              # Custom styles for the app
│   ├── database
│   │   ├── __init__.py        # Initializes the database module
│   │   ├── mongodb.py         # MongoDB connection and operations
│   │   └── models.py          # Data models for MongoDB collections
│   ├── rag
│   │   ├── __init__.py        # Initializes the RAG module
│   │   ├── retriever.py       # Functions for retrieving information
│   │   └── embeddings.py       # Functions for generating embeddings
│   ├── utils
│   │   ├── __init__.py        # Initializes the utils module
│   │   └── helpers.py         # Utility functions for the application
│   └── config.py              # Configuration settings
├── requirements.txt            # Project dependencies
├── .env.example                # Example environment variables
└── README.md                   # Project documentation
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd revisia
   ```

2. **Create a virtual environment:**
   ```
   python -m venv revisia
   source revisia/bin/activate  # On Windows use `revisia\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in the required values, such as database credentials.

5. **Run the application:**
   ```
   streamlit run src/main.py
   ```

## Usage
- Users can register and log in to access the chat interface.
- The chat interface allows users to send messages and view chat history.
- The application retrieves relevant information from the MongoDB database to enhance the chat experience.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.