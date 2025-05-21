from typing import Dict, List
import json
from app.services.llm.azure_openai_service import AzureOpenAIService

class CodeIdentificationAgent:
    """Agent responsible for identifying potential ICD and RxNorm codes from text"""
    
    SYSTEM_PROMPT = """You are a medical code identification specialist. Your task is to:
1. Analyze the medical text and identify potential medical codes
2. Separate codes into ICD-10 codes and RxNorm codes
3. Return only the identified codes in separate arrays

Be thorough in identifying potential codes but do not validate them yet."""

    def __init__(self):
        self.llm_service = AzureOpenAIService()

    def process(self, text: str) -> Dict[str, List[str]]:
        """
        Extract potential ICD and RxNorm codes from text.
        
        Args:
            text: The medical text to analyze
            
        Returns:
            Dictionary containing arrays of potential ICD and RxNorm codes
        """
        prompt = f"""Please analyze this medical text and identify potential medical codes:

Text:
{text}

For each medical concept mentioned (conditions, medications, procedures, etc.), identify potential:
1. ICD-10 codes for diagnoses and conditions
2. RxNorm codes for medications

Return ONLY the codes in this JSON format:
{{
    "icd_codes": ["list of potential ICD-10 codes"],
    "rxnorm_codes": ["list of potential RxNorm codes"]
}}"""

        result = self.llm_service.generate_text(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.0  # Use deterministic output for medical information
        )
        return json.loads(result["text"]) 