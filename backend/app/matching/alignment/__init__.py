"""Geometric alignment and ICP public API."""

from .config import ICPConfig
from .two_way import generate_candidates

__all__ = ["ICPConfig", "generate_candidates"]
