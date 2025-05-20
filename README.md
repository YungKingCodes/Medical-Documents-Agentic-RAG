# FastAPI Document API

A well-structured FastAPI application implementing a RAG (Retrieval Augmented Generation) system for document-based question answering, using Azure OpenAI for embeddings and text generation.

## Features

- Document storage and retrieval using SQLAlchemy
- RAG-based question answering using Azure OpenAI
- Vector storage using Chroma DB
- Efficient document chunking and retrieval
- Medical note summarization
- REST API endpoints for all functionality
- Automatic vector store processing for documents
- Transactional document management with rollback support

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

Copy the example environment file and modify as needed:

```bash
cp .env.example .env
```

3. Configure Azure OpenAI:

Add the following to your .env file:

```
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_EMBEDDINGS_API_KEY=your_azure_openai_embeddings_api_key  # Optional: If different from main API key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_EMBEDDING_ENDPOINT=your_azure_openai_embedding_endpoint  # Optional: If different from main endpoint
AZURE_OPENAI_MODEL=gpt-4o-mini  # Model type to use (gpt-4o-mini, gpt-4.1)
AZURE_OPENAI_DEPLOYMENT=deployment-name  # Optional: If specified, overrides AZURE_OPENAI_MODEL
AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-large  # Currently only supports text-embedding-3-large
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=embedding-deployment-name  # Optional: If specified, overrides AZURE_OPENAI_EMBEDDING_MODEL
```

4. Generate Vector Store Embeddings:

The vector store (Chroma DB) is not included in the repository due to its size. You need to generate the embeddings from the documents in the database:

```bash
python assets/generate_embeddings.py
```

This script will process all documents in the database and create the necessary embeddings in the `chroma_db` directory.

5. Run the server:

```bash
python main.py
# or
uvicorn app.main:app --reload
```

## Environment Variables

- `DATABASE_URL`: Database connection string (default: sqlite:///./documents.db)
- `DEBUG`: Set to True for development mode
- `API_KEY`: API key for authentication
- `SECRET_KEY`: Secret key for security
- `APP_NAME`: Name of the application (default: Document API)

### Azure OpenAI Configuration
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key for completion models
- `AZURE_OPENAI_EMBEDDINGS_API_KEY`: Azure OpenAI API key for embedding models (falls back to AZURE_OPENAI_API_KEY if not set)
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL for completions
- `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Azure OpenAI endpoint URL for embeddings (falls back to AZURE_OPENAI_ENDPOINT if not set)
- `AZURE_OPENAI_API_VERSION`: Azure OpenAI API version (default: 2023-05-15)
- `AZURE_OPENAI_MODEL`: Azure OpenAI model to use, values include:
  - `gpt-4o-mini`: GPT-4o Mini model (default)
  - `gpt-4.1`: GPT-4.1 model
- `AZURE_OPENAI_EMBEDDING_MODEL`: Azure OpenAI embedding model (text-embedding-3-large)

## API Endpoints

### Document Management
- `POST /api/v1/documents`: Create a new document
  - Automatically processes document for vector store
  - Rolls back creation if vector store processing fails
- `GET /api/v1/documents`: List all documents
- `GET /api/v1/documents/{id}`: Get a specific document
- `PUT /api/v1/documents/{id}`: Update a document
  - Automatically updates vector store embeddings
  - Deletes old embeddings before processing new ones
  - Rolls back changes if vector store processing fails
- `DELETE /api/v1/documents/{id}`: Delete a document
  - Automatically removes document embeddings from vector store
  - Ensures consistency between database and vector store

### Question Answering
- `POST /api/v1/answer_question`: Answer questions using RAG
  - Request body: `{"question": "your question here"}`
  - Returns: Answer and context from relevant document chunks

### Medical Notes
- `POST /api/v1/summarize_note`: Summarize medical notes
  - Request body: `{"note_text": "medical note content"}`
  - Returns: Structured summary of the medical note

## Sample API Calls

All endpoints require an API key to be passed in the header. Replace `your-api-key` with your actual API key.

### Document Management

1. Create a new document:
```bash
curl -X POST 'http://localhost:8000/api/v1/documents' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "title": "Sample Document",
    "content": "This is the content of the sample document."
  }'
```

2. List all documents:
```bash
curl -X GET 'http://localhost:8000/api/v1/documents' \
  -H 'X-API-Key: your-api-key'
```

3. Get a specific document:
```bash
curl -X GET 'http://localhost:8000/api/v1/documents/1' \
  -H 'X-API-Key: your-api-key'
```

4. Update a document:
```bash
curl -X PUT 'http://localhost:8000/api/v1/documents/1' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "title": "Updated Document",
    "content": "This is the updated content."
  }'
```

5. Delete a document:
```bash
curl -X DELETE 'http://localhost:8000/api/v1/documents/1' \
  -H 'X-API-Key: your-api-key'
```

### Question Answering

Ask a question about documents:
```bash
curl -X POST 'http://localhost:8000/api/v1/answer_question' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "question": "What is the main topic discussed in the documents?"
  }'
```

Example response:
```json
{
  "answer": "Based on the context, the main topic...",
  "context": {
    "chunks": [
      {
        "content": "...",
        "metadata": {
          "document_id": "1",
          "chunk_index": 0
        },
        "score": 0.89
      }
    ],
    "total_chunks_used": 1
  }
}
```

### Medical Notes

Summarize a medical note:
```bash
curl -X POST 'http://localhost:8000/api/v1/summarize_note' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "note_text": "Patient presented with fever and cough. Medical history includes hypertension..."
  }'
```

Example response:
```json
{
  "summary": "Demographics: Adult patient\nMedical History: Hypertension\nCurrent Symptoms: Fever, cough\n...",
  "processed_successfully": true,
  "error": null
}
```

## RAG System Configuration

The system uses the following configuration for document processing:

- Chunk size: 1000 characters
- Chunk overlap: 200 characters (20% overlap)
- Number of retrieved chunks: 3 (default)
- Embedding model: text-embedding-3-large
- Completion model: GPT-4o Mini (default) or GPT-4.1

This configuration is optimized for:
- Maintaining context between chunks
- Efficient retrieval of relevant information
- Balanced token usage within model limits
- Optimal response generation

### Vector Store Processing

Documents are automatically processed for the vector store:
- Documents are split into chunks with overlap
- Each chunk gets unique identifiers and metadata
- Embeddings are generated using Azure OpenAI
- Chunks are stored in Chroma DB for similarity search
- Old embeddings are automatically cleaned up on updates

## Development

The application uses:
- FastAPI for the web framework
- SQLAlchemy for database operations
- Chroma DB for vector storage
- Azure OpenAI for embeddings and text generation
- Pydantic for data validation
- Langchain for document processing