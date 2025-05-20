from fastapi import APIRouter
from app.schemas.user import UserBase
from app.models.user import UserModel
from app.services import user_service

router = APIRouter()

@router.get("/", response_model=list[str])
def get_users():
    return user_service.list_users()

@router.post("/", response_model=str)
def create_user(user: UserBase):
    new_user = user_service.create_user(user)
    return f"User created: {new_user.name} ({new_user.email})"
