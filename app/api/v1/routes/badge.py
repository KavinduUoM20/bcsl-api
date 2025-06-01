from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.core.auth import get_current_active_user, get_current_admin_user
from app.db.session import get_session
from app.services.badge_service import BadgeService
from app.schemas.badge import (
    BadgeCreate,
    BadgeUpdate,
    BadgeRead,
    MemberBadgeCreate,
    MemberBadgeUpdate,
    MemberBadgeRead
)
from app.models.user import User
from app.models.badge import MemberBadge

router = APIRouter()

@router.post("/", response_model=BadgeRead, status_code=status.HTTP_201_CREATED)
async def create_badge(
    badge_in: BadgeCreate,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new badge.
    Only admin users can access this endpoint.
    """
    badge_service = BadgeService(session)
    badge = await badge_service.create(badge_in)
    return badge

@router.get("/", response_model=List[BadgeRead])
async def list_badges(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = Query(False, description="Filter only active badges"),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieve badges with optional filters.
    All authenticated users can access this endpoint.
    """
    badge_service = BadgeService(session)
    badges = await badge_service.get_all(skip=skip, limit=limit, active_only=active_only)
    return badges

@router.get("/{badge_id}", response_model=BadgeRead)
async def get_badge(
    badge_id: UUID,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific badge by ID.
    All authenticated users can access this endpoint.
    """
    badge_service = BadgeService(session)
    badge = await badge_service.get(badge_id)
    if not badge:
        raise HTTPException(status_code=404, detail="Badge not found")
    return badge

@router.put("/{badge_id}", response_model=BadgeRead)
async def update_badge(
    badge_id: UUID,
    badge_in: BadgeUpdate,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a badge.
    Only admin users can access this endpoint.
    """
    badge_service = BadgeService(session)
    badge = await badge_service.get(badge_id)
    if not badge:
        raise HTTPException(status_code=404, detail="Badge not found")
    
    updated_badge = await badge_service.update(badge, badge_in)
    return updated_badge

@router.delete("/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_badge(
    badge_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a badge.
    Only admin users can access this endpoint.
    """
    badge_service = BadgeService(session)
    badge = await badge_service.get(badge_id)
    if not badge:
        raise HTTPException(status_code=404, detail="Badge not found")
    
    await badge_service.delete(badge)

@router.post("/assign", response_model=MemberBadgeRead)
async def assign_badge(
    member_badge_in: MemberBadgeCreate,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Assign a badge to a member.
    Only admin users can access this endpoint.
    """
    badge_service = BadgeService(session)
    member_badge = await badge_service.assign_badge(
        member_badge_in=member_badge_in,
        issued_by_id=current_user.id
    )
    return member_badge

@router.put("/member-badges/{member_badge_id}", response_model=MemberBadgeRead)
async def update_member_badge(
    member_badge_id: UUID,
    member_badge_in: MemberBadgeUpdate,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a member's badge (e.g., deactivate it).
    Only admin users can access this endpoint.
    """
    badge_service = BadgeService(session)
    # First get the member badge
    stmt = select(MemberBadge).where(MemberBadge.id == member_badge_id)
    result = await session.execute(stmt)
    member_badge = result.first()
    if not member_badge:
        raise HTTPException(status_code=404, detail="Member badge not found")
    
    updated_member_badge = await badge_service.update_member_badge(
        member_badge=member_badge[0],
        member_badge_in=member_badge_in
    )
    return updated_member_badge

@router.get("/members/{member_id}/badges", response_model=List[MemberBadgeRead])
async def get_member_badges(
    member_id: UUID,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = Query(False, description="Filter only active badges"),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get all badges for a specific member.
    All authenticated users can access this endpoint.
    """
    badge_service = BadgeService(session)
    member_badges = await badge_service.get_member_badges(
        member_id=member_id,
        skip=skip,
        limit=limit,
        active_only=active_only
    )
    return member_badges

@router.get("/{badge_id}/holders", response_model=List[MemberBadgeRead])
async def get_badge_holders(
    badge_id: UUID,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = Query(False, description="Filter only active badge holders"),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get all members who have a specific badge.
    All authenticated users can access this endpoint.
    """
    badge_service = BadgeService(session)
    badge_holders = await badge_service.get_badge_holders(
        badge_id=badge_id,
        skip=skip,
        limit=limit,
        active_only=active_only
    )
    return badge_holders

@router.delete("/members/{member_id}/badges/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member_badge(
    member_id: UUID,
    badge_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Remove a badge from a member.
    Only admin users can access this endpoint.
    """
    # First get the member badge
    stmt = select(MemberBadge).where(
        MemberBadge.member_id == member_id,
        MemberBadge.badge_id == badge_id,
        MemberBadge.is_active == True
    )
    result = await session.execute(stmt)
    member_badge = result.scalar_one_or_none()
    
    if not member_badge:
        raise HTTPException(
            status_code=404,
            detail="Active badge assignment not found for this member"
        )
    
    # Delete the member badge
    await session.delete(member_badge)
    await session.commit()
    
    return None 