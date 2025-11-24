from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
