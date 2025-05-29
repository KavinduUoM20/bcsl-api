from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.init_db import init_db
# from app.api.v1.routes import user
from app.api.v1.routes import company
from app.api.v1.routes import event
from app.api.v1.routes import member

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Server has been stopped")

version = "v1"

version_prefix =f"/api/{version}"

app = FastAPI(title="bcsl api", version=version, lifespan=lifespan)

# app.include_router(user.router, prefix=f"{version_prefix}/users", tags=["users"])
app.include_router(company.router, prefix=f"{version_prefix}/companies", tags=["companies"])
app.include_router(event.router, prefix=f"{version_prefix}/events", tags=["events"])
app.include_router(member.router, prefix=f"{version_prefix}/members", tags=["members"])