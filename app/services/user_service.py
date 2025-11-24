from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_in: UserCreate) -> User:
    stmt = select(User).where(User.login == user_in.login)
    existing = db.scalar(stmt)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this login already exists",
        )

    user = User(
        login=user_in.login,
        password_hash=hash_password(user_in.password),
        project_id=user_in.project_id,
        env=user_in.env.value,
        domain=user_in.domain.value,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session) -> List[User]:
    stmt = select(User)
    return list(db.scalars(stmt))


def get_user(db: Session, user_id: UUID) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


def acquire_lock(db: Session, user_id: UUID) -> User:
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.locktime is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already locked",
        )

    user.locktime = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def release_lock(db: Session, user_id: UUID) -> User:
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.locktime = None
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
