from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.db.models import Document
from app.schemas import DocumentCreate, DocumentUpdate, Document as DocumentSchema
from app.utils.security import get_api_key
from app.services.vector_store import vector_store_service

# Create router
router = APIRouter()

@router.get("/", response_model=List[DocumentSchema])
def get_documents(
    db: Session = Depends(get_db)
):
    """
    Get all documents.
    """
    return db.query(Document).all()

@router.post("/", response_model=DocumentSchema, status_code=201)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Create a new document.
    Requires API key.
    """
    # Create document in database
    db_document = Document(
        title=document.title,
        content=document.content
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    try:
        # Process document for vector store
        vector_store_service.process_document(
            document_id=str(db_document.id),
            content=db_document.content,
            metadata={"title": db_document.title}
        )
    except Exception as e:
        # If vector store processing fails, delete the document from database
        db.delete(db_document)
        db.commit()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document for vector store: {str(e)}"
        )
    
    return db_document

@router.get("/{document_id}", response_model=DocumentSchema)
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific document by ID.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.put("/{document_id}", response_model=DocumentSchema)
def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Update a document.
    Requires API key.
    """
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Store old content for rollback
    old_title = db_document.title
    old_content = db_document.content
    
    # Update document fields if provided
    if document_update.title is not None:
        db_document.title = document_update.title
    if document_update.content is not None:
        db_document.content = document_update.content
    
    try:
        # Delete old embeddings
        vector_store_service.delete_document(str(document_id))
        
        # Process updated document for vector store
        vector_store_service.process_document(
            document_id=str(document_id),
            content=db_document.content,
            metadata={"title": db_document.title}
        )
        
        # Commit database changes
        db.commit()
        db.refresh(db_document)
        
    except Exception as e:
        # Rollback changes if vector store processing fails
        db_document.title = old_title
        db_document.content = old_content
        db.commit()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process updated document for vector store: {str(e)}"
        )
    
    return db_document

@router.delete("/{document_id}", status_code=204)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Delete a document.
    Requires API key.
    """
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Delete document embeddings from vector store
        vector_store_service.delete_document(str(document_id))
        
        # Delete document from database
        db.delete(db_document)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )
    
    return None 