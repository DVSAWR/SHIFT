from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    user_name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    raising = Column(DateTime, nullable=False)
    salary = Column(Integer, nullable=False)
    token = Column(String, nullable=True, default=None)
    token_create_datetime = Column(DateTime, nullable=True, default=None)


SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
