from typing import Optional, List
from uuid import UUID
from datetime import datetime

from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, event_id: UUID) -> Optional[Event]:
        stmt = select(Event).where(Event.id == event_id)
        result = await self.session.execute(stmt)
        event_row = result.first()
        return event_row[0] if event_row else None

    async def get_all(self) -> List[Event]:
        stmt = select(Event).order_by(desc(Event.start_time))
        result = await self.session.execute(stmt)
        events = result.scalars().all()
        return events

    async def create(self, event_in: EventCreate) -> Event:
        data = event_in.model_dump()
        if data.get("cover_image_url"):
            data["cover_image_url"] = str(data["cover_image_url"])
        if data.get("registration_link"):
            data["registration_link"] = str(data["registration_link"])
        event = Event(**data)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def update(self, event: Event, event_in: EventUpdate) -> Event:
        event_data = event_in.model_dump(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        event.updated_at = datetime.utcnow()
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def delete(self, event: Event) -> None:
        await self.session.delete(event)
        await self.session.commit()
