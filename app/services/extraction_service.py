from typing import Dict, Any, Optional
from app.services.agents import (
    CodeIdentificationAgent,
    CodeLookupAgent,
    MedicalExtractionAgent
)
from app.schemas.extraction import (
    ExtractionResponse,
    StructuredMedicalData,
    PatientInfo,
    Condition,
    Medication,
    Treatment,
    Observation,
    PlanAction
)

class ExtractionService:
    """Service for extracting and enriching medical information from text"""
    
    def __init__(self):
        self.code_identifier = CodeIdentificationAgent()
        self.code_lookup = CodeLookupAgent()
        self.medical_extractor = MedicalExtractionAgent()
    
    def extract_entities(
        self,
        text: str,
    ) -> ExtractionResponse:
        """
        Process medical text through the agent pipeline.
        
        Args:
            text: The medical text to analyze
            
        Returns:
            ExtractionResponse containing structured medical information
        """
        # Step 1: Identify potential medical codes
        potential_codes = self.code_identifier.process(text)
        print(f"Potential codes: {potential_codes}")
        
        # Step 2: Look up and validate the codes
        code_mappings = self.code_lookup.process(potential_codes)
        print(f"Code mappings: {code_mappings}")
        
        # Step 3: Extract and enrich medical information
        raw_data = self.medical_extractor.process(text, code_mappings)
        print(f"Structured data: {raw_data}")
        
        # Convert raw data into proper Pydantic models
        structured_data = StructuredMedicalData(
            patient_info=PatientInfo(**raw_data["patient_info"]),
            conditions=[Condition(**c) for c in raw_data.get("conditions", [])],
            medications=[Medication(**m) for m in raw_data.get("medications", [])],
            treatments=[Treatment(**t) for t in raw_data.get("treatments", [])],
            observations=[Observation(**o) for o in raw_data.get("observations", [])],
            plan=[PlanAction(**p) for p in raw_data.get("plan", [])]
        )
        
        return ExtractionResponse(
            structured_data=structured_data,
            code_mappings=code_mappings,
            raw_codes=potential_codes
        )

# Create singleton instance
extraction_service = ExtractionService() 