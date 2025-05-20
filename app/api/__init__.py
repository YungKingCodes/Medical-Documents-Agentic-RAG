from fastapi import APIRouter

from app.api.endpoints import documents, medical

# Create API router
api_router = APIRouter()

# Include routers from endpoints
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(medical.router, prefix="/medical", tags=["medical"])
