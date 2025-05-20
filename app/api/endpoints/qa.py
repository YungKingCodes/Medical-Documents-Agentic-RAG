from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import llm_service

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    context: dict

@router.post("/answer_question", response_model=QuestionResponse)
async def answer_question(request: QuestionRequest):
    """
    Answer a question using RAG (Retrieval Augmented Generation).
    
    The endpoint retrieves relevant document chunks and uses them as context
    to generate an answer using the configured LLM.
    """
    try:
        result = llm_service.answer_question(request.question)
        return QuestionResponse(
            answer=result["answer"],
            context=result["context"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        ) 