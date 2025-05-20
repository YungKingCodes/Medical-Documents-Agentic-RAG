from fastapi import APIRouter, HTTPException, status
from app.schemas.medical import MedicalNoteRequest, MedicalNoteSummaryResponse
from app.services.llm.azure_openai_service import AzureOpenAIService
from app.services.llm.base_service import LLMServiceError

router = APIRouter()

@router.post(
    "/summarize_note", 
    response_model=MedicalNoteSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Summarize a medical note",
    description="Endpoint to summarize a medical note using Azure OpenAI."
)
async def summarize_medical_note(request: MedicalNoteRequest):
    """
    Summarize a medical note using Azure OpenAI.
    
    Args:
        request: The request containing the medical note text
        
    Returns:
        MedicalNoteSummaryResponse: The summarized medical note or error
    """
    # Create prompt for medical note summarization
    prompt = f"""
    You are a medical professional assistant. Please summarize the following medical note,
    extracting key patient information including:
    - Demographics
    - Medical history
    - Current symptoms
    - Diagnosis
    - Treatment plan
    
    Medical Note:
    {request.note_text}
    
    Format your response as a concise professional summary.
    """
    
    try:
        # Call Azure OpenAI to summarize the note
        llm_service = AzureOpenAIService()
        result = llm_service.generate_text(
            prompt=prompt,
            temperature=0.3,  # Lower temperature for more focused response
            max_tokens=500    # Limit the response length
        )
        
        # Return the response
        return MedicalNoteSummaryResponse(
            summary=result["text"],
            processed_successfully=True,
            error=None
        )
        
    except LLMServiceError as e:
        # Handle service errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process medical note: {str(e)}"
        )
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        ) 