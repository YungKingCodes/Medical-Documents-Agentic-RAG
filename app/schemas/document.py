from pydantic import BaseModel, ConfigDict
from typing import Optional

class DocumentBase(BaseModel):
    """Base schema for Document."""
    title: str
    content: str
    
class DocumentCreate(DocumentBase):
    """Schema for creating a Document."""
    pass

class DocumentUpdate(BaseModel):
    """Schema for updating a Document with optional fields."""
    title: Optional[str] = None
    content: Optional[str] = None

class Document(DocumentBase):
    """Schema for returning a Document."""
    id: int
    model_config = ConfigDict(from_attributes=True) 