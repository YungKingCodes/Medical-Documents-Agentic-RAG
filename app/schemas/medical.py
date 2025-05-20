from pydantic import BaseModel, Field

class MedicalNoteRequest(BaseModel):
    """Schema for medical note summarization request."""
    note_text: str = Field(..., description="The medical note to be summarized")

class MedicalNoteSummaryResponse(BaseModel):
    """Schema for medical note summarization response."""
    summary: str = Field(None, description="The summarized medical note")
    processed_successfully: bool = Field(..., description="Whether the note was processed successfully")
    error: str = Field(None, description="Error message if processing failed") 