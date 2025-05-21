from typing import List, Dict, Any, Tuple
import uuid
import json
from app.schemas.extraction import StructuredMedicalData
from app.services.llm_service import llm_service

class FHIRService:
    def __init__(self):
        self.llm = llm_service.llm_service

    def determine_fhir_resources(self, data: Dict[str, Any]) -> List[str]:
        """Use AI to determine which FHIR resources to generate based on the data"""
        prompt = f"""Given this medical data, determine which FHIR resources would best represent it.
        Focus on Patient, Condition, and MedicationStatement resources.
        Only return the resource types as a comma-separated list.
        
        Data: {json.dumps(data, indent=2)}
        """
        response = self.llm.generate_text(
            prompt=prompt,
            temperature=0,
            max_tokens=100,
            system_prompt="You are a FHIR expert. Return only the resource types as a comma-separated list without any additional text or explanation."
        )["text"].strip()
        return [r.strip() for r in response.split(",")]

    def generate_fhir_json(self, data: Dict[str, Any], resource_type: str) -> Dict[str, Any]:
        """Use AI to generate FHIR-compliant JSON for a specific resource type"""
        system_prompt = f"""You are a FHIR expert. Generate only valid FHIR JSON for a {resource_type} resource.
        The response must:
        1. Start with {{
        2. End with }}
        3. Be valid JSON
        4. Follow FHIR R4 specification
        5. Include only the JSON, no explanation or other text
        """
        
        prompt = f"""Convert this medical data into a valid FHIR {resource_type} resource.
        Follow these rules:
        1. Include only relevant fields from the data
        2. Use proper FHIR formatting and required fields
        3. Generate valid JSON that matches the FHIR R4 spec
        4. For references, use placeholder IDs
        5. Include proper coding systems (SNOMED, ICD, RxNorm) where applicable
        6. Ensure all JSON is properly formatted with correct brackets and commas
        
        Data: {json.dumps(data, indent=2)}
        """
        
        try:
            response = self.llm.generate_text(
                prompt=prompt,
                temperature=0,
                max_tokens=1000,
                system_prompt=system_prompt
            )["text"].strip()
            
            # Try to find JSON content if there's any extra text
            try:
                start_idx = response.index("{")
                end_idx = response.rindex("}") + 1
                response = response[start_idx:end_idx]
            except ValueError:
                raise ValueError(f"No valid JSON found in response for {resource_type}")
            
            # Parse and validate JSON
            try:
                fhir_json = json.loads(response)
                if not isinstance(fhir_json, dict):
                    raise ValueError("Response is not a JSON object")
                if "resourceType" not in fhir_json:
                    raise ValueError("Missing resourceType in FHIR resource")
                if fhir_json["resourceType"] != resource_type:
                    raise ValueError(f"Wrong resourceType: expected {resource_type}, got {fhir_json['resourceType']}")
                return fhir_json
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format: {str(e)}")
            
        except Exception as e:
            print(f"Error generating {resource_type} resource: {str(e)}")
            print(f"Raw response: {response}")
            raise ValueError(f"Failed to generate valid {resource_type} resource: {str(e)}")

    def convert_to_fhir(self, data: StructuredMedicalData) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Convert structured medical data to FHIR resources"""
        # Convert to dict for easier handling
        data_dict = data.dict()
        
        # Determine which FHIR resources to generate
        resource_types = self.determine_fhir_resources(data_dict)
        
        resources = []
        successful_types = []
        
        for resource_type in resource_types:
            try:
                fhir_json = self.generate_fhir_json(data_dict, resource_type)
                # Add a generated ID if none exists
                if "id" not in fhir_json:
                    fhir_json["id"] = str(uuid.uuid4())
                resources.append(fhir_json)
                successful_types.append(resource_type)
            except Exception as e:
                print(f"Error generating {resource_type}: {str(e)}")
                continue
                
        if not resources:
            raise ValueError("Failed to generate any valid FHIR resources")
                
        return resources, successful_types

fhir_service = FHIRService() 