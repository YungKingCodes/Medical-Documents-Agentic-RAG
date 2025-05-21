from fastapi import APIRouter

from app.api.endpoints import documents, medical, extraction, fhir

# Create API router
api_router = APIRouter()

# Include routers from endpoints
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(medical.router, prefix="/medical", tags=["medical"])
api_router.include_router(extraction.router, prefix="/extraction", tags=["extraction"])
api_router.include_router(fhir.router, prefix="/fhir", tags=["fhir"])
