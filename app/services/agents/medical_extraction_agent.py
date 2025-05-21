from typing import Dict, List, Any
import json
import logging
from app.services.llm.azure_openai_service import AzureOpenAIService
from app.services.llm.base_service import LLMServiceError
from app.schemas.extraction import ExtractionResponse

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MedicalExtractionAgent:
    """Agent responsible for extracting and enriching medical information"""
    
    SYSTEM_PROMPT = """You are a medical information extraction specialist. Your task is to:
1. Extract detailed medical information from the text
2. Enrich the information with provided code mappings
3. Create a comprehensive structured output
4. Include all relevant medical details and relationships

Be thorough and maintain accuracy in the extracted information.

IMPORTANT: Your response must be a valid JSON object matching the specified format exactly."""

    def __init__(self):
        self.llm_service = AzureOpenAIService()

    def process(self, text: str, code_mappings: Dict[str, List[Dict[str, str]]]) -> Dict[str, Any]:
        """
        Extract and enrich medical information.
        
        Args:
            text: The medical text to analyze
            code_mappings: Dictionary containing validated ICD and RxNorm code mappings
            
        Returns:
            Dictionary containing structured medical information
        """
        try:
            prompt = f"""Please analyze this medical text and create a structured representation:

Text:
{text}

Available Code Mappings:
{json.dumps(code_mappings, indent=2)}

Extract and structure the following information:
1. Patient Information
2. Conditions and Diagnoses (with ICD codes)
3. Medications (with RxNorm codes)
4. Treatments and Procedures
5. Vital Signs and Lab Results
6. Plan Actions and Follow-ups

Return ONLY a valid JSON object in this exact format:
{{
    "patient_info": {{
        "demographics": {{"age": "", "gender": "", "other_relevant_info": ""}},
        "medical_history": []
    }},
    "conditions": [
        {{
            "name": "condition name",
            "status": "status",
            "severity": "severity",
            "icd_code": "matched ICD code",
            "description": "from code mapping"
        }}
    ],
    "medications": [
        {{
            "name": "medication name",
            "dosage": "dosage",
            "frequency": "frequency",
            "route": "route",
            "rxnorm_code": "matched RxNorm code",
            "details": "from code mapping"
        }}
    ],
    "treatments": [
        {{
            "procedure": "procedure name",
            "status": "status",
            "date": "date"
        }}
    ],
    "observations": [
        {{
            "type": "observation type",
            "value": "value",
            "unit": "unit",
            "date": "date",
            "interpretation": "interpretation"
        }}
    ],
    "plan": [
        {{
            "action": "planned action",
            "due_date": "due date",
            "status": "status",
            "details": "additional details"
        }}
    ]
}}"""

            logger.debug("Sending prompt to LLM service")
            result = self.llm_service.generate_text(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                temperature=0.0  # Use deterministic output for medical information
            )
            
            logger.debug(f"Received response from LLM service: {result}")
            
            if not result.get("text"):
                raise ValueError("Empty response from LLM service")
                
            try:
                structured_data = json.loads(result["text"])
                logger.debug(f"Successfully parsed JSON response: {structured_data}")
                return structured_data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Raw response: {result['text']}")
                raise ValueError(f"Invalid JSON response from LLM: {str(e)}")
                
        except LLMServiceError as e:
            logger.error(f"LLM service error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in medical extraction: {e}")
            raise 