import datetime
import secrets

from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import User, get_db

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.put("/create_token")
async def create_token(user_name, password, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_name).first()
    if user is None:
        return JSONResponse(status_code=400, content={"message": "User not found"})
    if user.user_name == user_name and user.password == password:
        user.token = secrets.token_urlsafe(20)
        user.token_create_datetime = datetime.datetime.now()
        db.commit()
        db.refresh(user)
        return user.token, user.token_create_datetime
    else:
        return JSONResponse(status_code=401, content={"message": "Something wrong"})


@user_router.get("/get_raising_datetime/{user_name}")
async def get_raising_datetime(user_name, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_name).first()
    if user is None:
        return JSONResponse(status_code=400, content={"message": "User not found"})
    return user.raising


@user_router.get("/get_salary/{user_name}")
async def get_salary(user_name, password, token, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_name).first()

    if user is None:
        return JSONResponse(status_code=400, content={"message": "User not found"})
    if user.token != token \
            or (user.token_create_datetime + datetime.timedelta(seconds=10)) < datetime.datetime.now() \
            or user.password != password:
        return JSONResponse(status_code=401, content={"message": "Not valid token"})

    return user.salary
