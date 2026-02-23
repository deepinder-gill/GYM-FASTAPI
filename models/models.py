from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
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
    exercises = relationship("Workout_exercise", back_populates="owner")

class Workout_exercise(Base):
    __tablename__ = "Workout_Exercises"
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_name = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)
    owner = relationship("Workout_log", back_populates="exercises")

