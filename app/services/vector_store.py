from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from app.services.llm.azure_openai_service import AzureOpenAIEmbeddingService

class CustomEmbeddings:
    """Wrapper class to make Azure OpenAI embedding service compatible with LangChain's interface."""
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        result = self.embedding_service.generate_embeddings(texts=texts)
        return result["embeddings"]

    def embed_query(self, text: str) -> List[float]:
        """Embed a query."""
        result = self.embedding_service.generate_embeddings(texts=[text])
        return result["embeddings"][0]

class VectorStoreService:
    def __init__(self):
        embedding_service = AzureOpenAIEmbeddingService()
        self.embeddings = CustomEmbeddings(embedding_service)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = Chroma(
            collection_name="documents",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )

    def delete_document(self, document_id: str) -> None:
        """Delete all chunks belonging to a document from the vector store."""
        # Get all chunks for this document
        results = self.vector_store.similarity_search_with_score(
            "dummy query",  # The query doesn't matter as we'll filter by metadata
            k=1000,  # Set high to get all chunks
            filter={"document_id": document_id}
        )
        
        # Extract the ids of chunks to delete
        chunk_ids = [
            str(result[0].metadata.get("chunk_id"))
            for result in results
            if result[0].metadata.get("chunk_id") is not None
        ]
        
        if chunk_ids:
            # Delete the chunks
            self.vector_store._collection.delete(
                ids=chunk_ids
            )

    def process_document(self, document_id: str, content: str, metadata: Dict[str, Any] = None) -> None:
        """Process a document by splitting it into chunks and storing embeddings."""
        # Split document into chunks
        chunks = self.text_splitter.split_text(content)
        
        # Prepare metadata for each chunk
        chunk_metadata = []
        chunk_ids = []
        for i in range(len(chunks)):
            chunk_meta = metadata.copy() if metadata else {}
            chunk_id = f"{document_id}-chunk-{i}"
            chunk_meta.update({
                "document_id": document_id,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "chunk_id": chunk_id
            })
            chunk_metadata.append(chunk_meta)
            chunk_ids.append(chunk_id)

        # Add chunks to vector store
        self.vector_store.add_texts(
            texts=chunks,
            metadatas=chunk_metadata,
            ids=chunk_ids
        )

    def search_similar_chunks(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar chunks based on the query."""
        results = self.vector_store.similarity_search_with_score(
            query,
            k=k
        )
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            }
            for doc, score in results
        ]

vector_store_service = VectorStoreService() 