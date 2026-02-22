# Prompt Templates

Store reusable prompt templates here as plain text files.

## Naming Convention
- Use lowercase with underscores: `history_tutor.txt`
- Use `.txt` for simple prompts
- Use `.md` for prompts with rich formatting/documentation

## Placeholders
Use `{variable_name}` for dynamic content:
- `{question}` - User's question
- `{context}` - Retrieved context from RAG
- `{grade}` - Grade level
- `{page}` - Page reference

## Example Usage
```python
from rag.retriever import load_prompt_template

template = load_prompt_template("history_tutor.txt", default_fallback)
prompt = template.format(question=user_q, context=retrieved_docs)
```

## Best Practices
- Keep prompts under 500 tokens when possible
- Version control all changes
- Test prompt changes before deploying
- Document any special instructions in comments
