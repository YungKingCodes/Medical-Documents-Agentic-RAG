from sqlalchemy import Column, Integer, String, Text

from app.db.base import Base

class Document(Base):
    """SQLAlchemy model for documents table."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text) 