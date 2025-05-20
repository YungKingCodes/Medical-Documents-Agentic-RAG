from typing import List, Dict, Any
from app.services.vector_store import vector_store_service
from app.services.llm.azure_openai_service import AzureOpenAIService

class LLMService:
    MEDICAL_SYSTEM_PROMPT = "You are a medical assistant which summarizes medical SOAP notes. The user will provide a question and context will be retrieved from a vector store. If the answer cannot be found in the context, say so."
    
    def __init__(self):
        self.llm_service = AzureOpenAIService()

    def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question using RAG."""
        # Retrieve relevant chunks
        relevant_chunks = vector_store_service.search_similar_chunks(question)

        print(f"relevant_chunks: {relevant_chunks}")
        
        # Prepare context from chunks
        context = "\n\n".join([chunk["content"] for chunk in relevant_chunks])
        print(f"context: {context}")
        
        # Create prompt
        prompt = f"""
        Context:
        {context}

        Question: {question}

        Answer:"""
        
        # Get response from LLM
        result = self.llm_service.generate_text(
            prompt=prompt,
            temperature=0,  # Use 0 temperature for more deterministic answers
            max_tokens=1000,
            system_prompt=self.MEDICAL_SYSTEM_PROMPT
        )
        
        return {
            "answer": result["text"],
            "context": {
                "chunks": relevant_chunks,
                "total_chunks_used": len(relevant_chunks)
            }
        }

llm_service = LLMService() 