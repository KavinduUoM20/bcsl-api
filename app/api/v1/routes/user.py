from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import UUID

from app.core.auth import get_current_active_user, get_current_admin_user
from app.db.session import get_session
from app.services.user_service import UserService
from app.schemas.user import UserRead, UserUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieve users. Only accessible by admin users.
    """
    user_service = UserService(session)
    users = await user_service.get_all(skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get user by ID. Only accessible by admin users.
    """
    user_service = UserService(session)
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me", response_model=UserRead)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update current user.
    """
    user_service = UserService(session)
    updated_user = await user_service.update(current_user, user_update)
    return updated_user

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a user. Only accessible by admin users.
    """
    user_service = UserService(session)
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await user_service.update(user, user_update)
    return updated_user

@router.post("/me/enable-2fa/{method}")
async def enable_two_factor(
    method: str,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Enable two-factor authentication for current user.
    Method can be 'email' or 'sms'.
    """
    user_service = UserService(session)
    await user_service.enable_two_factor(current_user, method)
    return {"message": f"2FA enabled with {method} method"}
