from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.user import UserCreate, UserRead, LockResponse
from app.services.user_service import (
    create_user,
    get_users,
    acquire_lock,
    release_lock,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserRead, status_code=201)
def create_user_endpoint(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user_in)


@router.get("/", response_model=list[UserRead])
def list_users_endpoint(
    db: Session = Depends(get_db),
):
    return get_users(db)


@router.post("/{user_id}/acquire_lock", response_model=LockResponse)
def acquire_lock_endpoint(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    user = acquire_lock(db, user_id)
    return LockResponse(
        id=user.id,
        locked=user.locktime is not None,
        locktime=user.locktime,
    )


@router.post("/{user_id}/release_lock", response_model=LockResponse)
def release_lock_endpoint(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    user = release_lock(db, user_id)
    return LockResponse(
        id=user.id,
        locked=user.locktime is not None,
        locktime=user.locktime,
    )
