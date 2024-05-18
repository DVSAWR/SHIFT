from fastapi import FastAPI
from fastapi.responses import FileResponse

from database import engine, Base
from router_admin import admin_router
from router_user import user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin_router)
app.include_router(user_router)


@app.get("/")
async def main():
    return FileResponse("default.html")
