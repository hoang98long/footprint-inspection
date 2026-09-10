"""Database engine, unit-of-work dependency and development initialisation."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config.settings import settings
from app.database.base import Base

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialise_database() -> None:
    # Import models before metadata is evaluated.
    import app.models.case  # noqa: F401
    Base.metadata.create_all(bind=engine)
