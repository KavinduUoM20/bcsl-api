from fastapi import FastAPI
from db.init_db import init_db
from app.api.v1.routes import user
#from app.db.session import create_db_and_tables

version = "v1"

version_prefix =f"/api/{version}"

app = FastAPI(title="bcsl api", version=version)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user.router, prefix=f"{version_prefix}/users", tags=["users"])
