from typing import Dict, List
import json
from app.services.llm.azure_openai_service import AzureOpenAIService

class CodeLookupAgent:
    """Agent responsible for looking up and validating medical codes"""
    
    SYSTEM_PROMPT = """You are a medical coding specialist. Your task is to:
1. Look up and validate ICD-10 and RxNorm codes
2. Provide detailed descriptions for each valid code
3. Return comprehensive code mappings

Be precise and only return valid codes with accurate descriptions."""

    def __init__(self):
        self.llm_service = AzureOpenAIService()

    def process(self, code_arrays: Dict[str, List[str]]) -> Dict[str, List[Dict[str, str]]]:
        """
        Look up and validate medical codes.
        
        Args:
            code_arrays: Dictionary containing arrays of ICD and RxNorm codes to validate
            
        Returns:
            Dictionary containing validated code mappings with descriptions
        """
        prompt = f"""Please validate and look up these medical codes:

ICD-10 Codes:
{code_arrays["icd_codes"]}

RxNorm Codes:
{code_arrays["rxnorm_codes"]}

For each code, provide:
1. The code itself
2. The official description
3. Any relevant additional information

Return the results in this JSON format:
{{
    "icd_mappings": [
        {{
            "code": "ICD-10 code",
            "description": "official description",
            "category": "disease category"
        }}
    ],
    "rxnorm_mappings": [
        {{
            "code": "RxNorm code",
            "description": "medication name",
            "form": "dosage form",
            "strength": "strength info"
        }}
    ]
}}"""

        result = self.llm_service.generate_text(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.0  # Use deterministic output for medical information
        )
        return json.loads(result["text"]) 