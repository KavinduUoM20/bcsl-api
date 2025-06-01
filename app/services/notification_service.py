from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate

class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, notification_id: UUID) -> Optional[Notification]:
        stmt = select(Notification).where(Notification.id == notification_id)
        result = await self.session.execute(stmt)
        notification_row = result.first()
        return notification_row[0] if notification_row else None

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False,
        type: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Notification]:
        query = select(Notification).order_by(desc(Notification.created_at))
        
        # Apply filters
        if active_only:
            query = query.where(Notification.is_active == True)
        if type:
            query = query.where(Notification.type == type)
        if priority:
            query = query.where(Notification.priority == priority)
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        notifications = result.scalars().all()
        return list(notifications)

    async def create(self, notification_in: NotificationCreate) -> Notification:
        notification = Notification(**notification_in.model_dump())
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def update(self, notification: Notification, notification_in: NotificationUpdate) -> Notification:
        update_data = notification_in.model_dump(exclude_unset=True)
        
        # Update notification attributes
        for field, value in update_data.items():
            setattr(notification, field, value)
        
        notification.updated_at = datetime.utcnow()
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def delete(self, notification: Notification) -> None:
        await self.session.delete(notification)
        await self.session.commit()

    async def deactivate(self, notification: Notification) -> Notification:
        notification.is_active = False
        notification.updated_at = datetime.utcnow()
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def get_active_notifications(
        self,
        skip: int = 0,
        limit: int = 100,
        type: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Notification]:
        """Get active notifications that haven't expired."""
        query = select(Notification).where(
            Notification.is_active == True,
            (Notification.expires_at.is_(None) | (Notification.expires_at > datetime.utcnow()))
        ).order_by(desc(Notification.created_at))
        
        # Apply filters
        if type:
            query = query.where(Notification.type == type)
        if priority:
            query = query.where(Notification.priority == priority)
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        notifications = result.scalars().all()
        return list(notifications) 