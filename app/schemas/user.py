from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class EnvEnum(str, Enum):
    prod = "prod"
    preprod = "preprod"
    stage = "stage"


class DomainEnum(str, Enum):
    canary = "canary"
    regular = "regular"


class UserBase(BaseModel):
    login: EmailStr
    project_id: UUID
    env: EnvEnum
    domain: DomainEnum


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    locktime: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class LockResponse(BaseModel):
    id: UUID
    locked: bool
    locktime: Optional[datetime] = None
