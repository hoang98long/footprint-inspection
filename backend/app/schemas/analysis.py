"""Response contract for the footprint-analysis pipeline."""

from pydantic import BaseModel, Field


class Classification(BaseModel):
    category: str
    type: str
    material: str


class AnalysisRead(BaseModel):
    case_id: str
    status: str
    classification: Classification
    confidence: float = Field(ge=0, le=1)
