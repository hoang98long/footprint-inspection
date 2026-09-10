"""Request and response contracts for case management."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CaseStatus(StrEnum):
    NEW = "new"
    PROCESSING = "processing"
    REVIEW = "review"
    COMPLETED = "completed"
    NEEDS_INFORMATION = "needs_information"


class CaseCreate(BaseModel):
    id: str = Field(pattern=r"^HS-\d{4}-\d{4}$")
    title: str = Field(min_length=3, max_length=255)
    handling_unit: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=4000)


class CaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    handling_unit: str
    status: CaseStatus
    description: str | None
    created_at: datetime
    updated_at: datetime


class CaseList(BaseModel):
    items: list[CaseRead]
    total: int
