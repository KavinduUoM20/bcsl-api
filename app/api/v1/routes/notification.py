from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.core.auth import get_current_active_user, get_current_admin_user
from app.db.session import get_session
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationRead
from app.models.user import User
from app.schemas.notification import NotificationType, NotificationPriority

router = APIRouter()

@router.get("/", response_model=List[NotificationRead])
async def list_notifications(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = Query(False, description="Filter only active notifications"),
    type: Optional[NotificationType] = Query(None, description="Filter by notification type"),
    priority: Optional[NotificationPriority] = Query(None, description="Filter by priority"),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieve notifications with optional filters.
    All authenticated users can access this endpoint.
    """
    notification_service = NotificationService(session)
    notifications = await notification_service.get_all(
        skip=skip,
        limit=limit,
        active_only=active_only,
        type=type.value if type else None,
        priority=priority.value if priority else None
    )
    return notifications

@router.get("/active", response_model=List[NotificationRead])
async def list_active_notifications(
    skip: int = 0,
    limit: int = 100,
    type: Optional[NotificationType] = Query(None, description="Filter by notification type"),
    priority: Optional[NotificationPriority] = Query(None, description="Filter by priority"),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieve active and non-expired notifications.
    All authenticated users can access this endpoint.
    """
    notification_service = NotificationService(session)
    notifications = await notification_service.get_active_notifications(
        skip=skip,
        limit=limit,
        type=type.value if type else None,
        priority=priority.value if priority else None
    )
    return notifications

@router.get("/{notification_id}", response_model=NotificationRead)
async def get_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific notification by ID.
    All authenticated users can access this endpoint.
    """
    notification_service = NotificationService(session)
    notification = await notification_service.get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_in: NotificationCreate,
    current_user: User = Depends(get_current_admin_user),  # Only admins can create
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new notification.
    Only admin users can access this endpoint.
    """
    notification_service = NotificationService(session)
    notification = await notification_service.create(notification_in)
    return notification

@router.put("/{notification_id}", response_model=NotificationRead)
async def update_notification(
    notification_id: UUID,
    notification_in: NotificationUpdate,
    current_user: User = Depends(get_current_admin_user),  # Only admins can update
    session: AsyncSession = Depends(get_session)
):
    """
    Update a notification.
    Only admin users can access this endpoint.
    """
    notification_service = NotificationService(session)
    notification = await notification_service.get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    updated_notification = await notification_service.update(notification, notification_in)
    return updated_notification

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_admin_user),  # Only admins can delete
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a notification.
    Only admin users can access this endpoint.
    """
    notification_service = NotificationService(session)
    notification = await notification_service.get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    await notification_service.delete(notification)

@router.post("/{notification_id}/deactivate", response_model=NotificationRead)
async def deactivate_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_admin_user),  # Only admins can deactivate
    session: AsyncSession = Depends(get_session)
):
    """
    Deactivate a notification.
    Only admin users can access this endpoint.
    """
    notification_service = NotificationService(session)
    notification = await notification_service.get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    deactivated_notification = await notification_service.deactivate(notification)
    return deactivated_notification 