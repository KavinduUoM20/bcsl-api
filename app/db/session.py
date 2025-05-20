from sqlmodel import create_engine, Session
from typing import Generator
from core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
