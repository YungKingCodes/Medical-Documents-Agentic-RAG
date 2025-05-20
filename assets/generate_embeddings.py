import sys
import os
from pathlib import Path

# Add the parent directory to the Python path so we can import from app
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import get_db
from app.db.models import Document
from app.services.vector_store import vector_store_service

def generate_embeddings():
    """Generate embeddings for all documents in the database."""
    print("Starting embeddings generation...")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get all documents
        documents = db.query(Document).all()
        print(f"Found {len(documents)} documents in the database.")
        
        # Process each document
        for doc in documents:
            print(f"Processing document: {doc.title} (ID: {doc.id})")
            try:
                vector_store_service.process_document(
                    document_id=str(doc.id),
                    content=doc.content,
                    metadata={"title": doc.title}
                )
                print(f"Successfully processed document: {doc.title}")
            except Exception as e:
                print(f"Error processing document {doc.title}: {str(e)}")
        
        print("\nEmbeddings generation completed successfully!")
        
    except Exception as e:
        print(f"Error during embeddings generation: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_embeddings() 