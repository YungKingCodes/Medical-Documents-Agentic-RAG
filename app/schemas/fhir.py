from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from .extraction import StructuredMedicalData

class FHIRReference(BaseModel):
    """Reference to another FHIR resource"""
    reference: str = Field(..., description="Resource reference (e.g., 'Patient/123')")
    type: str = Field(..., description="Resource type")
    display: Optional[str] = Field(None, description="Display name")

class FHIRCodeableConcept(BaseModel):
    """FHIR codeable concept"""
    coding: List[Dict[str, str]] = Field(..., description="List of codes from different systems")
    text: Optional[str] = Field(None, description="Plain text representation")

class FHIRPatient(BaseModel):
    """Simplified FHIR Patient resource"""
    resourceType: Literal["Patient"] = "Patient"
    id: Optional[str] = Field(None)
    identifier: List[Dict[str, str]] = Field(default_factory=list)
    name: List[Dict[str, Any]] = Field(default_factory=list)
    gender: Optional[str] = Field(None)
    birthDate: Optional[str] = Field(None)

class FHIRCondition(BaseModel):
    """Simplified FHIR Condition resource"""
    resourceType: Literal["Condition"] = "Condition"
    id: Optional[str] = Field(None)
    subject: FHIRReference
    code: FHIRCodeableConcept
    severity: Optional[FHIRCodeableConcept] = Field(None)
    clinicalStatus: Optional[FHIRCodeableConcept] = Field(None)
    verificationStatus: Optional[FHIRCodeableConcept] = Field(None)
    onsetDateTime: Optional[str] = Field(None)

class FHIRMedicationStatement(BaseModel):
    """Simplified FHIR MedicationStatement resource"""
    resourceType: Literal["MedicationStatement"] = "MedicationStatement"
    id: Optional[str] = Field(None)
    subject: FHIRReference
    medicationCodeableConcept: FHIRCodeableConcept
    status: str = Field(..., description="active | completed | entered-in-error | intended | stopped | on-hold | unknown | not-taken")
    dosage: Optional[List[Dict[str, Any]]] = Field(None)

class ToFHIRRequest(BaseModel):
    """Request model for FHIR conversion"""
    structured_data: StructuredMedicalData = Field(..., description="Structured medical data to convert")

class ToFHIRResponse(BaseModel):
    """Response model for FHIR conversion"""
    resources: List[Dict[str, Any]] = Field(..., description="List of FHIR resources")
    resource_types: List[str] = Field(..., description="Types of resources generated") 