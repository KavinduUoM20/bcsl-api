from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_active_user, get_current_admin_user, get_current_moderator_user
from app.schemas.member import MemberCreate, MemberRead, MemberUpdate, MemberPublicRead
from app.schemas.social_link import SocialLinkCreate, SocialLinkRead
from app.schemas.external_link import ExternalLinkCreate, ExternalLinkRead
from app.services.member_service import MemberService
from app.db.session import get_session
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[MemberRead])
async def read_members(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all members with pagination.
    """
    service = MemberService(session)
    members = await service.get_all(skip=skip, limit=limit)
    return members


@router.get("/{member_id}", response_model=MemberRead)
async def read_member(
    member_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a specific member by ID.
    """
    service = MemberService(session)
    member = await service.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.get("/username/{username}", response_model=MemberRead)
async def read_member_by_username(
    username: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a member by username.
    """
    service = MemberService(session)
    member = await service.get_by_username(username)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.get("/slug/{slug}", response_model=MemberRead)
async def read_member_by_slug(
    slug: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a member by slug.
    """
    service = MemberService(session)
    member = await service.get_by_slug(slug)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.post("/", response_model=MemberRead, status_code=status.HTTP_201_CREATED)
async def create_member(
    member_in: MemberCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_moderator_user)
):
    """
    Create a new member.
    """
    service = MemberService(session)
    try:
        member = await service.create(member_in)
        return member
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{member_id}", response_model=MemberRead)
async def update_member(
    member_id: UUID,
    member_in: MemberUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a member's information. Users can update their own profile, moderators and admins can update any profile.
    """
    service = MemberService(session)
    member = await service.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Check if user has permission to update this member
    if current_user.member_id != member_id and current_user.role not in ["admin", "moderator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this member"
        )
    
    try:
        updated_member = await service.update(member, member_in)
        return updated_member
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(
    member_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete a member. Only accessible by admins.
    """
    service = MemberService(session)
    member = await service.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    await service.delete(member)
    return None


@router.get("/company/{company_id}", response_model=List[MemberRead])
async def read_company_members(
    company_id: UUID,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all members of a specific company with pagination.
    """
    service = MemberService(session)
    members = await service.get_by_company(company_id, skip=skip, limit=limit)
    return members


@router.post("/{member_id}/social-links", response_model=SocialLinkRead)
async def add_social_link(
    member_id: UUID,
    social_link: SocialLinkCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Add a social link to a member's profile. Users can only add to their own profile unless they are admin/moderator.
    """
    if current_user.member_id != member_id and current_user.role not in ["admin", "moderator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify this member's social links"
        )
    
    service = MemberService(session)
    return await service.add_social_link(
        member_id=member_id,
        title=social_link.title,
        link=social_link.link,
        icon=social_link.icon
    )


@router.post("/{member_id}/external-links", response_model=ExternalLinkRead)
async def add_external_link(
    member_id: UUID,
    external_link: ExternalLinkCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Add an external link to a member's profile. Users can only add to their own profile unless they are admin/moderator.
    """
    if current_user.member_id != member_id and current_user.role not in ["admin", "moderator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify this member's external links"
        )
    
    service = MemberService(session)
    return await service.add_external_link(
        member_id=member_id,
        title=external_link.title,
        link=external_link.link
    )


@router.post("/{follower_id}/follow/{followed_id}", status_code=status.HTTP_201_CREATED)
async def follow_member(
    follower_id: UUID,
    followed_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Follow another member. Users can only follow/unfollow using their own ID.
    """
    if current_user.member_id != follower_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only follow/unfollow using your own member ID"
        )
    
    service = MemberService(session)
    await service.follow_member(follower_id, followed_id)
    return {"message": "Successfully followed member"}


@router.delete("/{follower_id}/unfollow/{followed_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_member(
    follower_id: UUID,
    followed_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Unfollow a member. Users can only follow/unfollow using their own ID.
    """
    if current_user.member_id != follower_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only follow/unfollow using your own member ID"
        )
    
    service = MemberService(session)
    await service.unfollow_member(follower_id, followed_id)
    return None


@router.get("/{member_id}/followers", response_model=List[MemberPublicRead])
async def get_member_followers(
    member_id: UUID,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a member's followers with pagination.
    """
    service = MemberService(session)
    followers = await service.get_followers(member_id, skip=skip, limit=limit)
    return followers


@router.get("/{member_id}/following", response_model=List[MemberPublicRead])
async def get_member_following(
    member_id: UUID,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get members that a member is following with pagination.
    """
    service = MemberService(session)
    following = await service.get_following(member_id, skip=skip, limit=limit)
    return following 