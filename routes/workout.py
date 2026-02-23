from fastapi import APIRouter, HTTPException, Depends, Request
from app.Schemas.user import UserCreate, UserOut
from app.Schemas.workout import WorkoutLogOut, WorkoutExerciseOut, WorkoutLogCreate
from app.core.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, RefreshToken, WorkoutLog, WorkoutExercise
from app.core.dependencies import get_current_user
from jose import jwt, JWTError

workoutrouter = APIRouter()

@workoutrouter.post("/workouts", response_model=WorkoutLogOut)
def create_workout_log(
        log: WorkoutLogCreate ,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
    ):
    new_workout_log = WorkoutLog(
        user_id=current_user.id,
        note=log.note
    )
    db.add(new_workout_log)
    db.commit()
    db.refresh(new_workout_log)

    for ex in log.exercises:
        new_ex = WorkoutExercise(
            workout_id = new_workout_log.id,
            exercise_name = ex.exercise_name,
            sets = ex.sets,
            reps = ex.reps,
            weight = ex.weight
        )
        db.add(new_ex)
    db.flush()
    db.refresh(new_workout_log)

    return new_workout_log

