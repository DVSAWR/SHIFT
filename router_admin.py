import datetime

from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import User, get_db

admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.get("/get_all_users")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@admin_router.get("/get_user/{user_name}")
async def get_user(user_name, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_name).first()
    if user is None:
        return JSONResponse(status_code=400, content={"message": "User not found"})
    return user


@admin_router.post("/create_user")
async def create_user(full_name: str, user_name: str, password: str, salary: int, raising: str,
                      db: Session = Depends(get_db)):
    user = User(full_name=full_name,
                user_name=user_name,
                password=password,
                raising=datetime.datetime(*list(map(int, raising.split("_")))),
                salary=salary)
    if db.query(User).filter(User.user_name == user.user_name).first():
        return JSONResponse(status_code=400, content={"message": "Bad Request"})
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@admin_router.put("/update_user")
async def update_user(user_name, new_full_name, new_user_name, new_password, new_salary, new_raising: str,
                      db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_name).first()
    if user is None:
        return JSONResponse(status_code=400, content={"message": "User not found"})
    user.full_name = new_full_name
    user.user_name = new_user_name
    user.password = new_password
    user.salary = new_salary
    user.raising = datetime.datetime(*list(map(int, new_raising.split("_"))))
    db.commit()
    db.refresh(user)
    return user


@admin_router.delete("/delete_user/{user_name}")
async def delete_user(user_name, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_name).first()
    if user is None:
        return JSONResponse(status_code=400, content={"message": "User not found"})
    db.delete(user)
    db.commit()
    return user
