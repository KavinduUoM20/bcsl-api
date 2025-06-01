from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, validator
from enum import Enum

class NotificationType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"

class NotificationPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class NotificationBase(BaseModel):
    title: str
    message: str
    link: Optional[str] = None
    type: NotificationType
    priority: NotificationPriority = NotificationPriority.NORMAL
    is_active: bool = True
    expires_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    link: Optional[str] = None
    type: Optional[NotificationType] = None
    priority: Optional[NotificationPriority] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class NotificationRead(NotificationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime 