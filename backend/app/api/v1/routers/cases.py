from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.case import CaseCreate, CaseList, CaseRead
from app.services.case_service import case_service

router = APIRouter()


@router.get("", response_model=CaseList)
def list_cases(offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)) -> CaseList:
    items, total = case_service.list(db, offset, limit)
    return CaseList(items=items, total=total)


@router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)) -> CaseRead:
    return case_service.create(db, payload)
