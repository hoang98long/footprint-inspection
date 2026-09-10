"""Business rules for case management."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import cases as case_repository
from app.models.case import Case
from app.schemas.case import CaseCreate


class CaseService:
    def list(self, db: Session, offset: int, limit: int) -> tuple[list[Case], int]:
        return case_repository.list_cases(db, offset, limit)

    def create(self, db: Session, payload: CaseCreate) -> Case:
        if case_repository.get_case(db, payload.id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mã hồ sơ đã tồn tại.")
        return case_repository.create_case(db, payload)

    def get(self, db: Session, case_id: str) -> Case:
        case = case_repository.get_case(db, case_id)
        if not case:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy hồ sơ.")
        return case


case_service = CaseService()
