"""Flexible JSON-safe public contracts for Phase 2 matching output."""

from typing import Any
from pydantic import BaseModel


class MatchingData(BaseModel):
    alignment: dict[str, Any]
    similarity: dict[str, float | int]
    artifacts: dict[str, str]
    timing: dict[str, float]


class MatchingResponse(BaseModel):
    success: bool = True
    data: MatchingData
