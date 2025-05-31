from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Any, Optional
from datetime import datetime
import secrets

from app.core.auth import get_current_active_user
from app.db.session import get_session
from app.services.user_service import UserService
from app.services.member_service import MemberService
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.schemas.member import MemberCreate
from app.models.user import User

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
) -> dict[str, Any]:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user_service = UserService(session)
    user = await user_service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Update last login timestamp
    await user_service.update_last_login(user)
    
    # Create access token
    access_token = user_service.create_access_token(user.id, user.member_id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    *,
    user_in: UserCreate,
    member_in: Optional[MemberCreate] = None,
    session: AsyncSession = Depends(get_session)
) -> Any:
    """
    Create new user with optional member profile.
    If member details are not provided, a basic member profile will be created.
    """
    # Create a basic member if no member details provided
    member_service = MemberService(session)
    if member_in is None:
        # Generate a unique username from email
        base_username = user_in.email.split('@')[0]
        username = base_username
        counter = 1
        while True:
            try:
                # Check if username exists
                existing = await member_service._check_unique_constraints(username=username)
                if not existing:
                    break
                username = f"{base_username}{counter}"
                counter += 1
            except Exception:
                username = f"{base_username}{secrets.token_hex(4)}"
                break

        # Create basic member with minimal info
        member_in = MemberCreate(
            first_name=base_username,
            last_name="",
            user_name=username,
            slug=username.lower(),
            wallet_key=f"temp_{secrets.token_hex(16)}",  # Temporary wallet key
            joined_at=datetime.utcnow(),
            email=user_in.email  # Set email from user
        )
    else:
        # If member details were provided, ensure email is set
        member_in_dict = member_in.model_dump()
        member_in_dict['email'] = user_in.email
        member_in = MemberCreate(**member_in_dict)
    
    try:
        # Create the member first
        member = await member_service.create(member_in)
        
        # Then create the user with the member_id
        user_service = UserService(session)
        user = await user_service.create(user_in, member.id)
        
        return user
    except HTTPException as e:
        # If user creation fails, clean up the member
        if 'member' in locals():
            await member_service.delete(member)
        raise e
    except Exception as e:
        # If user creation fails, clean up the member
        if 'member' in locals():
            await member_service.delete(member)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify-email/{token}")
async def verify_email(
    token: str,
    session: AsyncSession = Depends(get_session)
) -> dict[str, str]:
    """
    Verify user's email address.
    """
    try:
        # Implement email verification token validation logic here
        # This is a placeholder that needs to be implemented based on your email verification strategy
        raise NotImplementedError("Email verification not implemented")
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/request-password-reset")
async def request_password_reset(
    email: str,
    session: AsyncSession = Depends(get_session)
) -> dict[str, str]:
    """
    Request a password reset for a user.
    """
    user_service = UserService(session)
    user = await user_service.get_by_email(email)
    if user:
        # Implement password reset email sending logic here
        # This is a placeholder that needs to be implemented based on your email service
        pass
    return {"message": "If a user with that email exists, a password reset link has been sent."}

@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user.
    """
    return current_user 