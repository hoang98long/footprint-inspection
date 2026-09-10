from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.analysis import AnalysisRead
from app.services.analysis_service import analysis_service
from app.services.case_service import case_service

router = APIRouter()


@router.get("/{case_id}/analysis", response_model=AnalysisRead)
def get_analysis(case_id: str, db: Session = Depends(get_db)) -> AnalysisRead:
    case_service.get(db, case_id)
    return analysis_service.analyse_case(case_id)
