from app.models.user import UserModel
from app.schemas.user import UserBase

def create_user(user_data: UserBase) -> UserModel:
    # Simulate business logic / transformation
    user = UserModel(name=user_data.name, email=user_data.email)
    return user

def list_users() -> list[str]:
    # Simulate a static list for now
    return ["Alice", "Bob", "Charlie"]
