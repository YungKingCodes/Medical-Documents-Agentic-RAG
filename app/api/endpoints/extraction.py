from fastapi import APIRouter, HTTPException, status
from app.schemas.extraction import ExtractionRequest, ExtractionResponse
from app.services.extraction_service import extraction_service

router = APIRouter()

@router.post(
    "/extract",
    response_model=ExtractionResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract medical entities and codes",
    description="Extract medical entities and codes from text using AI."
)
async def extract_medical_entities(request: ExtractionRequest) -> ExtractionResponse:
    """
    Extract medical entities and codes from text.
    
    Args:
        request: ExtractionRequest containing the text to analyze
        
    Returns:
        ExtractionResponse containing extracted entities and code mappings
        
    Raises:
        HTTPException: If extraction fails
    """
    try:
        return extraction_service.extract_entities(text=request.text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting medical entities: {str(e)}"
        ) 