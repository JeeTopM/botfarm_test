from datetime import datetime
import enum
import uuid

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class EnvEnum(str, enum.Enum):
    prod = "prod"
    preprod = "preprod"
    stage = "stage"


class DomainEnum(str, enum.Enum):
    canary = "canary"
    regular = "regular"


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    login = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    project_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )
    env = Column(Enum(EnvEnum), nullable=False)
    domain = Column(Enum(DomainEnum), nullable=False)
    locktime = Column(DateTime, nullable=True)
