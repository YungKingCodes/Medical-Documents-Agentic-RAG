from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.db.base import engine
import app.db.models as models
from app.api.endpoints import qa

# Create database tables
models.Document.__table__.create(bind=engine, checkfirst=True)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Interview API",
    description="API for question answering using RAG",
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

@app.get("/")
async def root():
    return {"message": "Welcome to RAG Interview API"} 