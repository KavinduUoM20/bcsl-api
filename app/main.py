from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from app.core.config import settings
from app.api.v1.routes import auth, user, company, event, member, notification, badge  # Import notification and badge routes
from app.db.session import engine
# Import models for table creation
from app.models.user import User
from app.models.member import Member
from app.models.company import Company
from app.models.follower import Follower
from app.models.social_link import SocialLink
from app.models.external_link import ExternalLink
from app.models.image import Image
from app.models.notification import Notification  # Import notification model
from app.models.badge import Badge, MemberBadge  # Import badge models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="v1",
    lifespan=lifespan
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
api_v1_prefix = f"{settings.API_V1_STR}"
app.include_router(auth.router, prefix=f"{api_v1_prefix}/auth", tags=["auth"])
app.include_router(user.router, prefix=f"{api_v1_prefix}/users", tags=["users"])
app.include_router(company.router, prefix=f"{api_v1_prefix}/companies", tags=["companies"])
app.include_router(event.router, prefix=f"{api_v1_prefix}/events", tags=["events"])
app.include_router(member.router, prefix=f"{api_v1_prefix}/members", tags=["members"])
app.include_router(notification.router, prefix=f"{api_v1_prefix}/notifications", tags=["notifications"])
app.include_router(badge.router, prefix=f"{api_v1_prefix}/badges", tags=["badges"])