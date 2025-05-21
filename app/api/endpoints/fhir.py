from fastapi import APIRouter, HTTPException, status
from app.schemas.fhir import ToFHIRRequest, ToFHIRResponse
from app.services.fhir_service import fhir_service

router = APIRouter()

@router.post(
    "/to_fhir",
    response_model=ToFHIRResponse,
    status_code=status.HTTP_200_OK,
    summary="Convert structured data to FHIR resources",
    description="Convert extracted medical data into FHIR-compliant resources using AI."
)
async def convert_to_fhir(request: ToFHIRRequest) -> ToFHIRResponse:
    """
    Convert structured medical data to FHIR resources.
    
    Args:
        request: ToFHIRRequest containing the structured medical data
        
    Returns:
        ToFHIRResponse containing FHIR resources and their types
        
    Raises:
        HTTPException: If conversion fails
    """
    try:
        resources, resource_types = fhir_service.convert_to_fhir(request.structured_data)
        return ToFHIRResponse(
            resources=resources,
            resource_types=resource_types
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting to FHIR: {str(e)}"
        ) 