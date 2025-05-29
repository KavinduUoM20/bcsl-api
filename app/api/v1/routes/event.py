from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.event import EventCreate, EventRead, EventUpdate
from app.services.event_service import EventService
from app.db.session import get_session

router = APIRouter()

@router.get("/", response_model=List[EventRead])
async def read_events(session: AsyncSession = Depends(get_session)):
    service = EventService(session)
    events = await service.get_all()
    return events


@router.get("/{event_id}", response_model=EventRead)
async def read_event(event_id: UUID, session: AsyncSession = Depends(get_session)):
    service = EventService(session)
    event = await service.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(event_in: EventCreate, session: AsyncSession = Depends(get_session)):
    service = EventService(session)
    event = await service.create(event_in)
    return event


@router.put("/{event_id}", response_model=EventRead)
async def update_event(event_id: UUID, event_in: EventUpdate, session: AsyncSession = Depends(get_session)):
    service = EventService(session)
    event = await service.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event = await service.update(event, event_in)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: UUID, session: AsyncSession = Depends(get_session)):
    service = EventService(session)
    event = await service.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    await service.delete(event)
    return None
