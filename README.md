# Medical Documents Agentic RAG

A FastAPI-based application implementing an intelligent medical information extraction system using specialized agents and Azure OpenAI for processing medical documents. The system uses a RAG (Retrieval Augmented Generation) approach combined with medical code identification and validation.

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

## Agentic Medical Info Extraction

- Medical information extraction using specialized agents:
  - Code identification for ICD-10 and RxNorm codes
  - Code validation and lookup with detailed descriptions
  - Comprehensive medical information extraction

## Development

The application uses:
- FastAPI for the web framework
- SQLAlchemy for database operations
- Chroma DB for vector storage
- Azure OpenAI for embeddings and text generation
- Pydantic for data validation
- Langchain for document processing

## Architecture

The system uses three specialized agents working in a pipeline:

1. **Code Identification Agent**
   - Takes raw medical text as input
   - Identifies potential ICD-10 and RxNorm codes
   - Returns arrays of potential codes without validation

2. **Code Lookup Agent**
   - Takes arrays of potential codes from first agent
   - Validates and looks up code descriptions
   - Returns detailed mappings with descriptions and metadata

3. **Medical Extraction Agent**
   - Takes raw text and validated code mappings
   - Extracts comprehensive medical information
   - Enriches extracted data with code mappings
   - Returns structured data including:
     - Patient information
     - Conditions with ICD codes
     - Medications with RxNorm codes
     - Treatments and procedures
     - Observations and vital signs
     - Plan actions and follow-ups

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

```bash
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

```bash
python assets/generate_embeddings.py
```

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
- `APP_NAME`: Name of the application (default: Medical Documents API)

### Azure OpenAI Configuration
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key for completion models
- `AZURE_OPENAI_EMBEDDINGS_API_KEY`: Azure OpenAI API key for embedding models (falls back to AZURE_OPENAI_API_KEY if not set)
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL for completions
- `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Azure OpenAI endpoint URL for embeddings (falls back to AZURE_OPENAI_ENDPOINT if not set)
- `AZURE_OPENAI_API_VERSION`: Azure OpenAI API version (default: 2023-05-15)
- `AZURE_OPENAI_MODEL`: Azure OpenAI model to use
- `AZURE_OPENAI_EMBEDDING_MODEL`: Azure OpenAI embedding model (text-embedding-3-large)

## API Endpoints

### Medical Information Extraction
- `POST /api/v1/extract`: Extract medical information from text
  - Request body: `{"text": "medical text content"}`
  - Returns: Structured medical information including:
    - Identified medical codes (ICD-10, RxNorm)
    - Validated code mappings with descriptions
    - Comprehensive medical information extraction
    - Patient demographics and history
    - Conditions, medications, and treatments
    - Observations and plan actions

### FHIR Conversion
- `POST /api/v1/fhir/to_fhir`: Convert structured medical data to FHIR resources
  - Request body: Structured medical data from the extraction endpoint
  - Returns: FHIR-compliant resources including:
    - Automatically determined resource types (Patient, Condition, MedicationStatement)
    - Valid FHIR JSON for each resource
    - Proper coding systems (SNOMED, ICD, RxNorm)
    - Resource references and relationships
  - Example response:
    ```json
    {
      "resources": [
        {
          "resourceType": "Patient",
          "id": "example-id",
          "name": [...],
          "gender": "male",
          "birthDate": "1970-01-01"
        },
        {
          "resourceType": "Condition",
          "id": "condition-id",
          "subject": {
            "reference": "Patient/example-id"
          },
          "code": {
            "coding": [
              {
                "system": "http://snomed.info/sct",
                "code": "13645005",
                "display": "Chronic obstructive lung disease"
              }
            ]
          }
        }
      ],
      "resource_types": ["Patient", "Condition"]
    }
    ```

### Question Answering
- `POST /api/v1/qa`: Answer questions about medical documents
  - Request body: 
    ```json
    {
      "question": "What medications is the patient taking?",
      "context": "optional document ID or text to focus search",
      "top_k": "optional number of documents to retrieve (default: 3)"
    }
    ```
  - Returns: Answer with supporting context and document references

### Document Management
- `POST /api/v1/documents`: Create a new document
- `GET /api/v1/documents`: List all documents
- `GET /api/v1/documents/{id}`: Get a specific document
- `PUT /api/v1/documents/{id}`: Update a document
- `DELETE /api/v1/documents/{id}`: Delete a document

## Sample API Calls

All endpoints require an API key to be passed in the header. Replace `your-api-key` with your actual API key.

### Medical Information Extraction

1. Extract medical information from text:
```bash
curl -X POST 'http://localhost:8000/api/v1/extract' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "text": "SOAP Note - Encounter Date: 2023-10-26\nPatient: patient--001\n\nS: Pt presents today for annual physical check-up. No chief complaints. Reports generally good health, denies chest pain, SOB, HA, dizziness. Family hx of elevated cholesterol (dad), no significant personal PMH issues reported. States routine exercise (~2x/wk), balanced diet but with occasional fast-food. Denies tobacco use, reports occasional ETOH socially.\n\nO:\nVitals:\n\nBP: 128/82 mmHg\nHR: 72 bpm, regular\nRR: 16 breaths/min\nTemp: 98.2Â°F oral\nHt: 5'\''10\", Wt: 192 lbs, BMI: 27.5 (overweight)\nGeneral appearance: Alert, NAD, pleasant and cooperative.\nSkin: Clear, normal moisture/turgor\nHEENT: PERRLA, EOMI, no scleral icterus. Oral mucosa moist, throat clear, no erythema\nCV: Regular rate & rhythm, no murmurs, rubs or gallops\nLungs: CTA bilaterally, no wheezing or crackles\nABD: Soft, NT/ND, bowel sounds normal\nNeuro: CN II-XII intact, normal strength & sensation bilat\nEXT: No edema, pulses +2 bilaterally\nLabs ordered: CBC, CMP, Lipid panel\n\nA:\n\nAdult annual health exam, generally healthy\nPossible overweight (BMI 27.5), recommend lifestyle modifications\nFamily hx of hyperlipidemia, screening initiated\nP:\n\nAdvised pt on healthier diet, increasing weekly exercise frequency to at least 3-4 times/week\nScheduled follow-up visit to review lab results and cholesterol levels in approx. 5 months\nRoutine annual influenza vaccine administered today - tolerated well\nNo Rx prescribed at this visit.\n\nSigned:\nDr. Mark Reynolds, MD\nInternal Medicine"
  }'
```

Example response:
```json
{
  "structured_data": {
    "patient_info": {
      "demographics": {
        "age": "",
        "gender": "",
        "other_relevant_info": "BMI: 27.5 (overweight)"
      },
      "medical_history": ["Family history of elevated cholesterol"]
    },
    "conditions": [
      {
        "name": "overweight",
        "status": "current",
        "severity": "mild",
        "icd_code": "E66.3",
        "description": "Overweight"
      }
    ],
    "medications": [],
    "treatments": [
      {
        "procedure": "influenza vaccine",
        "status": "completed",
        "date": "2023-10-26"
      }
    ],
    "observations": [
      {
        "type": "blood pressure",
        "value": "128/82",
        "unit": "mmHg",
        "date": "2023-10-26",
        "interpretation": "normal"
      },
      {
        "type": "heart rate",
        "value": "72",
        "unit": "bpm",
        "date": "2023-10-26",
        "interpretation": "regular"
      },
      {
        "type": "respiratory rate",
        "value": "16",
        "unit": "breaths/min",
        "date": "2023-10-26",
        "interpretation": "normal"
      },
      {
        "type": "temperature",
        "value": "98.2",
        "unit": "°F",
        "date": "2023-10-26",
        "interpretation": "normal"
      },
      {
        "type": "BMI",
        "value": "27.5",
        "unit": "kg/m2",
        "date": "2023-10-26",
        "interpretation": "overweight"
      }
    ],
    "plan": [
      {
        "action": "lifestyle modification",
        "due_date": "",
        "status": "recommended",
        "details": "Increase exercise frequency to 3-4 times/week, improve diet"
      },
      {
        "action": "follow-up visit",
        "due_date": "2024-03-26",
        "status": "scheduled",
        "details": "Review lab results and cholesterol levels"
      },
      {
        "action": "laboratory tests",
        "due_date": "",
        "status": "ordered",
        "details": "CBC, CMP, Lipid panel"
      }
    ]
  },
  "code_mappings": {
    "icd_mappings": [
      {
        "code": "E66.3",
        "description": "Overweight",
        "category": "Endocrine, nutritional and metabolic diseases"
      }
    ],
    "rxnorm_mappings": []
  },
  "raw_codes": {
    "icd_codes": ["E66.3"],
    "rxnorm_codes": []
  }
}
```

### FHIR Conversion

1. Convert structured medical data to FHIR resources:
```bash
curl -X POST 'http://localhost:8000/api/v1/fhir/to_fhir' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "structured_data": {
      "patient_info": {
        "demographics": {
          "age": "",
          "gender": "",
          "other_relevant_info": "BMI: 27.5 (overweight)"
        },
        "medical_history": ["Family history of elevated cholesterol"]
      },
      "conditions": [
        {
          "name": "overweight",
          "status": "current",
          "severity": "mild",
          "icd_code": "E66.3",
          "description": "Overweight"
        }
      ],
      "medications": [],
      "treatments": [
        {
          "procedure": "influenza vaccine",
          "status": "completed",
          "date": "2023-10-26"
        }
      ],
      "observations": [
        {
          "type": "blood pressure",
          "value": "128/82",
          "unit": "mmHg",
          "date": "2023-10-26",
          "interpretation": "normal"
        },
        {
          "type": "heart rate",
          "value": "72",
          "unit": "bpm",
          "date": "2023-10-26",
          "interpretation": "regular"
        },
        {
          "type": "respiratory rate",
          "value": "16",
          "unit": "breaths/min",
          "date": "2023-10-26",
          "interpretation": "normal"
        },
        {
          "type": "temperature",
          "value": "98.2",
          "unit": "°F",
          "date": "2023-10-26",
          "interpretation": "normal"
        },
        {
          "type": "BMI",
          "value": "27.5",
          "unit": "kg/m2",
          "date": "2023-10-26",
          "interpretation": "overweight"
        }
      ],
      "plan": [
        {
          "action": "lifestyle modification",
          "due_date": "",
          "status": "recommended",
          "details": "Increase exercise frequency to 3-4 times/week, improve diet"
        },
        {
          "action": "follow-up visit",
          "due_date": "2024-03-26",
          "status": "scheduled",
          "details": "Review lab results and cholesterol levels"
        },
        {
          "action": "laboratory tests",
          "due_date": "",
          "status": "ordered",
          "details": "CBC, CMP, Lipid panel"
        }
      ]
    },
    "code_mappings": {
      "icd_mappings": [
        {
          "code": "E66.3",
          "description": "Overweight",
          "category": "Endocrine, nutritional and metabolic diseases"
        }
      ],
      "rxnorm_mappings": []
    },
    "raw_codes": {
      "icd_codes": ["E66.3"],
      "rxnorm_codes": []
    }
  }'
```

Example response:
```json
{
  "resources": [
    {
      "resourceType": "Patient",
      "id": "example-id",
      "name": [...],
      "gender": "male",
      "birthDate": "1970-01-01"
    },
    {
      "resourceType": "Condition",
      "id": "condition-id",
      "subject": {
        "reference": "Patient/example-id"
      },
      "code": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "13645005",
            "display": "Chronic obstructive lung disease"
          }
        ]
      }
    }
  ],
  "resource_types": ["Patient", "Condition"]
}
```

### Question Answering

1. Ask a question about medical documents:
```bash
curl -X POST 'http://localhost:8000/api/v1/qa' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "question": "What medications is the patient taking for hypertension?",
    "top_k": 3
  }'
```

Example response:
```json
{
  "answer": "According to the medical records, the patient is taking lisinopril 10mg daily for hypertension.",
  "confidence": 0.92,
  "context": {
    "relevant_documents": [
      {
        "content": "Patient is a 45-year-old male with hypertension (ICD-10: I10) taking lisinopril 10mg daily...",
        "document_id": 1,
        "relevance_score": 0.95,
        "metadata": {
          "title": "Medical Note - John Doe",
          "date": "2024-03-20"
        }
      }
    ],
    "total_documents_searched": 3
  },
  "medical_codes": {
    "medications": [
      {
        "name": "lisinopril",
        "rxnorm_code": "29046",
        "dosage": "10mg",
        "frequency": "daily"
      }
    ],
    "conditions": [
      {
        "name": "hypertension",
        "icd_code": "I10"
      }
    ]
  }
}
```

2. Ask a question about a specific document:
```bash
curl -X POST 'http://localhost:8000/api/v1/qa' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "question": "What was the patient's last blood pressure reading?",
    "context": "1",  # Document ID
    "top_k": 1
  }'
```

Example response:
```json
{
  "answer": "The patient's last blood pressure reading was 120/80.",
  "confidence": 0.95,
  "context": {
    "relevant_documents": [
      {
        "content": "...Updated with new blood pressure readings...",
        "document_id": 1,
        "relevance_score": 0.98,
        "metadata": {
          "title": "Medical Note - John Doe (Updated)",
          "date": "2024-03-20",
          "last_bp": "120/80"
        }
      }
    ],
    "total_documents_searched": 1
  }
}
```

### Document Management

1. Create a new document:
```bash
curl -X POST 'http://localhost:8000/api/v1/documents' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "title": "Medical Note - John Doe",
    "content": "Patient is a 45-year-old male with hypertension (ICD-10: I10) taking lisinopril 10mg daily...",
    "metadata": {
      "patient_id": "12345",
      "date": "2024-03-20",
      "provider": "Dr. Smith"
    }
  }'
```

Example response:
```json
{
  "id": 1,
  "title": "Medical Note - John Doe",
  "content": "Patient is a 45-year-old male with hypertension...",
  "metadata": {
    "patient_id": "12345",
    "date": "2024-03-20",
    "provider": "Dr. Smith"
  },
  "created_at": "2024-03-20T10:30:00Z",
  "updated_at": "2024-03-20T10:30:00Z"
}
```

2. List all documents:
```bash
# Basic listing
curl -X GET 'http://localhost:8000/api/v1/documents' \
  -H 'X-API-Key: your-api-key'

# With pagination
curl -X GET 'http://localhost:8000/api/v1/documents?page=1&per_page=10' \
  -H 'X-API-Key: your-api-key'

# With filters
curl -X GET 'http://localhost:8000/api/v1/documents?search=hypertension&date_from=2024-01-01' \
  -H 'X-API-Key: your-api-key'
```

Example response:
```json
{
  "items": [
    {
      "id": 1,
      "title": "Medical Note - John Doe",
      "content": "Patient is a 45-year-old male...",
      "metadata": {
        "patient_id": "12345",
        "date": "2024-03-20",
        "provider": "Dr. Smith"
      },
      "created_at": "2024-03-20T10:30:00Z",
      "updated_at": "2024-03-20T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "total_pages": 1
}
```

3. Get a specific document:
```bash
curl -X GET 'http://localhost:8000/api/v1/documents/1' \
  -H 'X-API-Key: your-api-key'
```

Example response:
```json
{
  "id": 1,
  "title": "Medical Note - John Doe",
  "content": "Patient is a 45-year-old male with hypertension...",
  "metadata": {
    "patient_id": "12345",
    "date": "2024-03-20",
    "provider": "Dr. Smith"
  },
  "created_at": "2024-03-20T10:30:00Z",
  "updated_at": "2024-03-20T10:30:00Z"
}
```

4. Update a document:
```bash
curl -X PUT 'http://localhost:8000/api/v1/documents/1' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "title": "Medical Note - John Doe (Updated)",
    "content": "Patient is a 45-year-old male with hypertension (ICD-10: I10) taking lisinopril 10mg daily. Updated with new blood pressure readings.",
    "metadata": {
      "patient_id": "12345",
      "date": "2024-03-20",
      "provider": "Dr. Smith",
      "last_bp": "120/80"
    }
  }'
```

Example response:
```json
{
  "id": 1,
  "title": "Medical Note - John Doe (Updated)",
  "content": "Patient is a 45-year-old male with hypertension...",
  "metadata": {
    "patient_id": "12345",
    "date": "2024-03-20",
    "provider": "Dr. Smith",
    "last_bp": "120/80"
  },
  "created_at": "2024-03-20T10:30:00Z",
  "updated_at": "2024-03-20T11:15:00Z"
}
```

5. Delete a document:
```bash
curl -X DELETE 'http://localhost:8000/api/v1/documents/1' \
  -H 'X-API-Key: your-api-key'
```

Example response:
```json
{
  "message": "Document deleted successfully",
  "document_id": 1
}
```

## 🐳 Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Environment Setup
1. Create a `.env` file in the root directory with the following variables:
```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DOCUMENTS_DB_PATH=/app/documents.db
CHROMA_DB_PATH=/app/chroma_db

# Application Settings
DEBUG=False
LOG_LEVEL=INFO

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
```

### Building and Running
1. Build the Docker images:
```bash
docker-compose build
```

2. Start the services:
```bash
docker-compose up
```

The API will be available at:
- FastAPI Application: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- ChromaDB (if needed): http://localhost:8001

### Development Mode
The application runs with hot-reload enabled by default. Any changes to the code in the `app` directory will automatically trigger a reload of the application.

### Persistent Storage
The following data is persisted across container restarts:
- SQLite database: `./documents.db`
- ChromaDB data: `./chroma_db/`

### Stopping the Services
To stop the services:
```bash
docker-compose down
```

### Troubleshooting
1. If you encounter permission issues with the database files, ensure the correct permissions:
```bash
chmod 666 documents.db
chmod -R 777 chroma_db/
```

2. If the services don't start properly, check the logs:
```bash
docker-compose logs -f
```