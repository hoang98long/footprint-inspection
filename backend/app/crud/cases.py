"""Database access layer for case files."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.case import Case
from app.schemas.case import CaseCreate


def list_cases(db: Session, offset: int = 0, limit: int = 50) -> tuple[list[Case], int]:
    items = db.scalars(select(Case).order_by(Case.updated_at.desc()).offset(offset).limit(limit)).all()
    total = db.scalar(select(func.count()).select_from(Case)) or 0
    return list(items), total


def get_case(db: Session, case_id: str) -> Case | None:
    return db.get(Case, case_id)


def create_case(db: Session, payload: CaseCreate) -> Case:
    case = Case(**payload.model_dump())
    db.add(case)
    db.commit()
    db.refresh(case)
    return case
