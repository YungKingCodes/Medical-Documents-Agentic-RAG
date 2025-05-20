from app.schemas.document import Document, DocumentBase, DocumentCreate, DocumentUpdate
from app.schemas.medical import MedicalNoteRequest, MedicalNoteSummaryResponse

# Add schemas to this import to make them easier to import elsewhere
__all__ = [
    "Document", "DocumentBase", "DocumentCreate", "DocumentUpdate",
    "MedicalNoteRequest", "MedicalNoteSummaryResponse"
]
