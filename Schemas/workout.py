from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WorkoutLogCreate(BaseModel):
    note : Optional[str] = None
    exercises : List[WorkoutExerciseCreate]

class WorkoutLogOut(BaseModel):
    id : int
    user_id : int
    created_at : datetime
    note : Optional[str] = None
    exercises : List[WorkoutExerciseOut]

    class Config:
        orm_mode = True

class WorkoutExerciseCreate(BaseModel):
    exercise_name : str
    sets : int
    reps : int
    weight : float

class WorkoutExerciseOut(BaseModel):
    id : int
    exercise_name : str
    sets : int
    reps : int
    weight : float

    class Config:
        orm_mode =True



