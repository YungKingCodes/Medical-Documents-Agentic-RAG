"""Schema models for the application."""

from app.schemas.document import Document, DocumentCreate, DocumentUpdate
from app.schemas.medical import MedicalNoteRequest, MedicalNoteSummaryResponse
from app.schemas.extraction import (
    ExtractionRequest,
    ExtractionResponse,
    PatientInfo,
    Condition,
    Medication,
    Treatment,
    Observation,
    PlanAction,
    StructuredMedicalData
)

# Add schemas to this import to make them easier to import elsewhere
__all__ = [
    "Document",
    "DocumentCreate",
    "DocumentUpdate",
    "MedicalNoteRequest",
    "MedicalNoteSummaryResponse",
    "ExtractionRequest",
    "ExtractionResponse",
    "PatientInfo",
    "Condition",
    "Medication",
    "Treatment",
    "Observation",
    "PlanAction",
    "StructuredMedicalData"
]
