"""Orchestration boundary for the AI footprint-analysis workflow."""

from app.schemas.analysis import AnalysisRead, Classification


class AnalysisService:
    def analyse_case(self, case_id: str) -> AnalysisRead:
        # TODO: invoke preprocessing, feature extraction and matching pipeline.
        # The typed response preserves a stable frontend contract until inference is wired.
        return AnalysisRead(case_id=case_id, status="queued", classification=Classification(category="Chưa phân loại", type="Chưa xác định", material="Chưa xác định"), confidence=0.0)


analysis_service = AnalysisService()
