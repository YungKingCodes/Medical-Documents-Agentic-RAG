from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.db.base import engine
import app.db.models as models
from app.api.endpoints import qa, medical, extraction

# Create database tables
models.Document.__table__.create(bind=engine, checkfirst=True)

# Initialize FastAPI app
app = FastAPI(
    title="Medical Documents API",
    description="API for processing and analyzing medical documents using RAG and structured extraction",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Include QA router
app.include_router(qa.router, prefix="/api/v1", tags=["qa"])

# Include Medical router
app.include_router(medical.router, prefix="/api/v1", tags=["medical"])

# Include Extraction router
app.include_router(extraction.router, prefix="/api/v1", tags=["extraction"])

@app.get("/")
async def root():
    return {"message": "Welcome to Medical Documents API"} 