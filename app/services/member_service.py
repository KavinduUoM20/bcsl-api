from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlalchemy import or_
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from app.models.member import Member
from app.models.social_link import SocialLink
from app.models.external_link import ExternalLink
from app.models.follower import Follower
from app.schemas.member import MemberCreate, MemberUpdate


class MemberService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, member_id: UUID) -> Optional[Member]:
        stmt = select(Member).where(Member.id == member_id)
        result = await self.session.execute(stmt)
        member_row = result.first()
        return member_row[0] if member_row else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Member]:
        stmt = select(Member).order_by(desc(Member.created_at)).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        members = result.scalars().all()
        return list(members)

    async def get_by_email(self, email: str) -> Optional[Member]:
        stmt = select(Member).where(Member.email == email)
        result = await self.session.execute(stmt)
        member_row = result.first()
        return member_row[0] if member_row else None

    async def get_by_username(self, username: str) -> Optional[Member]:
        stmt = select(Member).where(Member.user_name == username)
        result = await self.session.execute(stmt)
        member_row = result.first()
        return member_row[0] if member_row else None

    async def get_by_slug(self, slug: str) -> Optional[Member]:
        stmt = select(Member).where(Member.slug == slug)
        result = await self.session.execute(stmt)
        member_row = result.first()
        return member_row[0] if member_row else None

    async def get_by_wallet(self, wallet_key: str) -> Optional[Member]:
        stmt = select(Member).where(Member.wallet_key == wallet_key)
        result = await self.session.execute(stmt)
        member_row = result.first()
        return member_row[0] if member_row else None

    async def create(self, member_in: MemberCreate) -> Member:
        # Check for unique constraints
        existing = await self._check_unique_constraints(
            email=member_in.email,
            username=member_in.user_name,
            slug=member_in.slug,
            wallet_key=member_in.wallet_key
        )
        if existing:
            raise HTTPException(status_code=400, detail=existing)

        member = Member(**member_in.model_dump())
        if not member.joined_at:
            member.joined_at = datetime.utcnow()

        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member

    async def update(self, member: Member, member_in: MemberUpdate) -> Member:
        # Check unique constraints if relevant fields are being updated
        if any([member_in.email, member_in.user_name, member_in.slug, member_in.wallet_key]):
            existing = await self._check_unique_constraints(
                email=member_in.email if member_in.email and member_in.email != member.email else None,
                username=member_in.user_name if member_in.user_name and member_in.user_name != member.user_name else None,
                slug=member_in.slug if member_in.slug and member_in.slug != member.slug else None,
                wallet_key=member_in.wallet_key if member_in.wallet_key and member_in.wallet_key != member.wallet_key else None
            )
            if existing:
                raise HTTPException(status_code=400, detail=existing)

        member_data = member_in.model_dump(exclude_unset=True)
        for key, value in member_data.items():
            setattr(member, key, value)
        
        member.updated_at = datetime.utcnow()
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member

    async def delete(self, member: Member) -> None:
        await self.session.delete(member)
        await self.session.commit()

    async def get_by_company(self, company_id: UUID, skip: int = 0, limit: int = 100) -> List[Member]:
        stmt = select(Member).where(Member.company_id == company_id).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        members = result.scalars().all()
        return list(members)

    async def add_social_link(self, member_id: UUID, title: str, link: str, icon: str) -> SocialLink:
        member = await self.get(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        social_link = SocialLink(title=title, link=link, icon=icon, member_id=member_id)
        self.session.add(social_link)
        await self.session.commit()
        await self.session.refresh(social_link)
        return social_link

    async def add_external_link(self, member_id: UUID, title: str, link: str) -> ExternalLink:
        member = await self.get(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        external_link = ExternalLink(title=title, link=link, member_id=member_id)
        self.session.add(external_link)
        await self.session.commit()
        await self.session.refresh(external_link)
        return external_link

    async def follow_member(self, follower_id: UUID, followed_id: UUID) -> Follower:
        if follower_id == followed_id:
            raise HTTPException(status_code=400, detail="Cannot follow yourself")
        
        # Check if both members exist
        follower = await self.get(follower_id)
        followed = await self.get(followed_id)
        if not follower or not followed:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Check if already following
        stmt = select(Follower).where(
            Follower.follower_id == follower_id,
            Follower.followed_id == followed_id
        )
        result = await self.session.execute(stmt)
        if result.first():
            raise HTTPException(status_code=400, detail="Already following this member")
        
        follower_rel = Follower(follower_id=follower_id, followed_id=followed_id)
        self.session.add(follower_rel)
        await self.session.commit()
        await self.session.refresh(follower_rel)
        return follower_rel

    async def unfollow_member(self, follower_id: UUID, followed_id: UUID) -> None:
        stmt = select(Follower).where(
            Follower.follower_id == follower_id,
            Follower.followed_id == followed_id
        )
        result = await self.session.execute(stmt)
        follower_rel = result.first()
        if not follower_rel:
            raise HTTPException(status_code=404, detail="Not following this member")
        
        await self.session.delete(follower_rel[0])
        await self.session.commit()

    async def _check_unique_constraints(
        self,
        email: Optional[str] = None,
        username: Optional[str] = None,
        slug: Optional[str] = None,
        wallet_key: Optional[str] = None
    ) -> Optional[str]:
        """Check unique constraints and return error message if violated."""
        conditions = []
        if email:
            conditions.append(Member.email == email)
        if username:
            conditions.append(Member.user_name == username)
        if slug:
            conditions.append(Member.slug == slug)
        if wallet_key:
            conditions.append(Member.wallet_key == wallet_key)
        
        if conditions:
            stmt = select(Member).where(or_(*conditions))
            result = await self.session.execute(stmt)
            existing = result.first()
            if existing:
                member = existing[0]
                if email and member.email == email:
                    return "Email already registered"
                if username and member.user_name == username:
                    return "Username already taken"
                if slug and member.slug == slug:
                    return "Slug already exists"
                if wallet_key and member.wallet_key == wallet_key:
                    return "Wallet key already registered"
        return None
