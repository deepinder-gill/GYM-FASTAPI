from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from datetime import datetime, timezone

from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    workout_logs = relationship("WorkoutLog", back_populates="user")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

class WorkoutLog(Base):

    __tablename__ = "workout_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    note = Column(String, nullable=True)

    exercises = relationship("WorkoutExercise", back_populates="workout")
    user = relationship("User", back_populates="workout_logs")

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workout_logs.id"))
    exercise_name = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)

    workout = relationship("WorkoutLog", back_populates="exercises")


