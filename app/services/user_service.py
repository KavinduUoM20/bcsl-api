from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, user_id: UUID, member_id: UUID) -> str:
        to_encode = {
            "sub": str(user_id),
            "member_id": str(member_id),
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    async def get(self, user_id: UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user_row = result.first()
        return user_row[0] if user_row else None

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        user_row = result.first()
        return user_row[0] if user_row else None

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user

    async def create(self, user_in: UserCreate, member_id: UUID) -> User:
        """Create a new user."""
        # Check if email already exists
        existing = await self._check_unique_constraints(email=user_in.email)
        if existing:
            raise HTTPException(status_code=400, detail=existing)

        # Hash the password
        hashed_password = self.get_password_hash(user_in.password)
        
        # Create user object
        user_data = user_in.model_dump()
        user_data.pop("password")  # Remove plain password
        user = User(
            **user_data,
            member_id=member_id,
            password_hash=hashed_password
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User, user_in: UserUpdate) -> User:
        update_data = user_in.model_dump(exclude_unset=True)
        
        # If email is being updated, check it's not taken
        if "email" in update_data and update_data["email"] != user.email:
            existing_user = await self.get_by_email(update_data["email"])
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")

        # Hash new password if provided
        if "password" in update_data:
            update_data["password_hash"] = self.get_password_hash(update_data.pop("password"))

        # Update user attributes
        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_at = datetime.utcnow()
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_last_login(self, user: User) -> None:
        user.last_login = datetime.utcnow()
        self.session.add(user)
        await self.session.commit()

    async def verify_email(self, user: User) -> None:
        user.email_verified = True
        self.session.add(user)
        await self.session.commit()

    async def verify_phone(self, user: User) -> None:
        user.phone_verified = True
        self.session.add(user)
        await self.session.commit()

    async def enable_two_factor(self, user: User, method: str) -> None:
        if method not in ["email", "sms"]:
            raise HTTPException(status_code=400, detail="Invalid 2FA method")
        user.two_factor_enabled = True
        user.two_factor_method = method
        self.session.add(user)
        await self.session.commit()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        stmt = select(User).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return list(users)

    async def _check_unique_constraints(self, email: Optional[str] = None) -> Optional[str]:
        """Check unique constraints and return error message if violated."""
        if email:
            stmt = select(User).where(User.email == email)
            result = await self.session.execute(stmt)
            existing = result.first()
            if existing:
                return "Email already registered"
        return None
