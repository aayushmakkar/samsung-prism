# AI Disclosure

This project uses AI-assisted development and AI services as part of the prototype.

## Development Assistance

AI assistants were used to support implementation, debugging, code structuring, documentation, and development workflow.

The final implementation was reviewed and tested locally by the project team.

## Runtime AI

The application uses the Groq API for language-model-based:

- Multi-intent query decomposition
- Grounded answer generation

## Retrieval

The retrieval pipeline uses:

- Sentence Transformers for text embeddings
- FAISS for local vector similarity search

## Human Oversight

The project team designed the system architecture, selected the retrieval and control flow, tested the implementation, and reviewed the generated outputs.

AI-generated outputs are constrained by retrieved evidence in the RAG pipeline.