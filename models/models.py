from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

class Workout_log(Base):

    __tablename__ = "workout_logs"
    id = Column(Integer, primary_key=True, index=True)
    users_id = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime, default=datetime.now)
    note = Column(String, nullable=True)
    posts = relationship()

cl
