from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ExtractionRequest(BaseModel):
    """Request model for medical text extraction"""
    text: str = Field(..., description="Medical text to analyze")

class PatientInfo(BaseModel):
    """Patient information"""
    demographics: Dict[str, str] = Field(..., description="Patient demographic information")
    medical_history: List[str] = Field(default_factory=list, description="Patient medical history")

class Condition(BaseModel):
    """Medical condition information"""
    name: str = Field(..., description="Name of the condition")
    status: str = Field(None, description="Status of the condition")
    severity: str = Field(None, description="Severity of the condition")
    icd_code: str = Field(None, description="Associated ICD code")
    description: str = Field(None, description="Description from code mapping")

class Medication(BaseModel):
    """Medication information"""
    name: str = Field(..., description="Name of the medication")
    dosage: str = Field(None, description="Medication dosage")
    frequency: str = Field(None, description="Medication frequency")
    route: str = Field(None, description="Route of administration")
    rxnorm_code: str = Field(None, description="Associated RxNorm code")
    details: str = Field(None, description="Details from code mapping")

class Treatment(BaseModel):
    """Treatment or procedure information"""
    procedure: str = Field(..., description="Name of the procedure")
    status: str = Field(None, description="Status of the procedure")
    date: str = Field(None, description="Date of the procedure")

class Observation(BaseModel):
    """Medical observation"""
    type: str = Field(..., description="Type of observation")
    value: str = Field(..., description="Observed value")
    unit: str = Field(None, description="Unit of measurement")
    date: str = Field(None, description="Date of observation")
    interpretation: str = Field(None, description="Interpretation of the result")

class PlanAction(BaseModel):
    """Planned medical action"""
    action: str = Field(..., description="Planned action")
    due_date: str = Field(None, description="Due date")
    status: str = Field(None, description="Status of the plan")
    details: str = Field(None, description="Additional details")

class StructuredMedicalData(BaseModel):
    """Structured medical information"""
    patient_info: PatientInfo = Field(..., description="Patient information")
    conditions: List[Condition] = Field(default_factory=list, description="List of conditions")
    medications: List[Medication] = Field(default_factory=list, description="List of medications")
    treatments: List[Treatment] = Field(default_factory=list, description="List of treatments")
    observations: List[Observation] = Field(default_factory=list, description="List of observations")
    plan: List[PlanAction] = Field(default_factory=list, description="List of planned actions")

class ExtractionResponse(BaseModel):
    """Response model for medical text extraction"""
    structured_data: StructuredMedicalData = Field(..., description="Structured medical information")
    code_mappings: Dict[str, List[Dict[str, str]]] = Field(..., description="Validated code mappings")
    raw_codes: Dict[str, List[str]] = Field(..., description="Raw identified codes before validation") 