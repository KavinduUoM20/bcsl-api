from typing import Optional, List
from uuid import UUID
from datetime import datetime
import pytz
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from app.models.badge import Badge, MemberBadge
from app.models.member import Member
from app.schemas.badge import BadgeCreate, BadgeUpdate, MemberBadgeCreate, MemberBadgeUpdate


class BadgeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, badge_in: BadgeCreate) -> Badge:
        """Create a new badge."""
        badge = Badge(**badge_in.model_dump())
        self.session.add(badge)
        await self.session.commit()
        await self.session.refresh(badge)
        return badge

    async def get(self, badge_id: UUID) -> Optional[Badge]:
        """Get a badge by ID."""
        stmt = select(Badge).where(Badge.id == badge_id)
        result = await self.session.execute(stmt)
        badge_row = result.first()
        return badge_row[0] if badge_row else None

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[Badge]:
        """Get all badges with optional filtering."""
        query = select(Badge)
        if active_only:
            query = query.where(Badge.is_active == True)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, badge: Badge, badge_in: BadgeUpdate) -> Badge:
        """Update a badge."""
        update_data = badge_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(badge, field, value)
        
        badge.updated_at = datetime.now(pytz.UTC)
        self.session.add(badge)
        await self.session.commit()
        await self.session.refresh(badge)
        return badge

    async def delete(self, badge: Badge) -> None:
        """Delete a badge."""
        await self.session.delete(badge)
        await self.session.commit()

    async def assign_badge(
        self,
        member_badge_in: MemberBadgeCreate,
        issued_by_id: UUID
    ) -> MemberBadge:
        """Assign a badge to a member."""
        # Check if member exists
        stmt = select(Member).where(Member.id == member_badge_in.member_id)
        result = await self.session.execute(stmt)
        member = result.scalar_one_or_none()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        # Check if badge is active
        badge = await self.get(member_badge_in.badge_id)
        if not badge:
            raise HTTPException(status_code=404, detail="Badge not found")
        if not badge.is_active:
            raise HTTPException(status_code=400, detail="Badge is not active")
        
        # Check if badge is valid (within valid_from and valid_until dates)
        now = datetime.now(pytz.UTC)
        if badge.valid_from > now:
            raise HTTPException(status_code=400, detail="Badge is not yet valid")
        if badge.valid_until and badge.valid_until < now:
            raise HTTPException(status_code=400, detail="Badge has expired")

        # Check if member already has this badge
        stmt = select(MemberBadge).where(
            MemberBadge.member_id == member_badge_in.member_id,
            MemberBadge.badge_id == member_badge_in.badge_id
        )
        result = await self.session.execute(stmt)
        if result.first():
            raise HTTPException(status_code=400, detail="Member already has this badge")

        # Create member badge
        member_badge = MemberBadge(
            **member_badge_in.model_dump(),
            issued_by_id=issued_by_id,
            issued_at=now  # Use UTC time for issued_at
        )
        self.session.add(member_badge)
        await self.session.commit()
        await self.session.refresh(member_badge)
        return member_badge

    async def update_member_badge(
        self,
        member_badge: MemberBadge,
        member_badge_in: MemberBadgeUpdate
    ) -> MemberBadge:
        """Update a member's badge (e.g., deactivate it)."""
        update_data = member_badge_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(member_badge, field, value)
        
        self.session.add(member_badge)
        await self.session.commit()
        await self.session.refresh(member_badge)
        return member_badge

    async def get_member_badges(
        self,
        member_id: UUID,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[MemberBadge]:
        """Get all badges for a specific member."""
        query = select(MemberBadge).where(MemberBadge.member_id == member_id)
        if active_only:
            query = query.where(MemberBadge.is_active == True)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_badge_holders(
        self,
        badge_id: UUID,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[MemberBadge]:
        """Get all members who have a specific badge."""
        query = select(MemberBadge).where(MemberBadge.badge_id == badge_id)
        if active_only:
            query = query.where(MemberBadge.is_active == True)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()) 