from fastapi import APIRouter, HTTPException, Depends, Request
from app.Schemas.user import UserCreate, UserOut
from app.Schemas.workout import WorkoutLogOut, WorkoutExerciseOut, WorkoutLogCreate
from app.core.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, RefreshToken, WorkoutLog, WorkoutExercise
from app.core.dependencies import get_current_user
from jose import jwt, JWTError
from collections import Counter

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
    db.flush()
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
    db.commit()
    db.refresh(new_workout_log)

    return new_workout_log

@workoutrouter.get("/workouts", response_model=list[WorkoutLogOut] )
def get_all_workouts(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
    ):
    logs = db.query(WorkoutLog).filter(WorkoutLog.user_id == current_user.id).all()
    return logs



@workoutrouter.get("/workouts/analytics")
def workout_analytics(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    workouts = db.query(WorkoutLog).filter(
        WorkoutLog.user_id == current_user.id
    ).all()

    all_exercises = []

    for workout in workouts:
        for exercise in workout.exercises:
            all_exercises.append(exercise)

    total_volume = 0
    for ex in all_exercises:
        total_volume += ex.sets * ex.reps * ex.weight

    exercise_count = Counter(ex.exercise_name for ex in all_exercises)
    most_trained  = exercise_count.most_common(1)[0][0]

    personal_record = {}
    for ex in all_exercises:
        if ex.exercise_name not in personal_record:
            personal_record[ex.exercise_name] = ex.weight

        else:
            if ex.weight > personal_record[ex.exercise_name]:
                personal_record[ex.exercise_name] = ex.weight

    return {
        "total_workouts": len(workouts),
        "total_volume_kg": total_volume,
        "most_trained_exercise": most_trained,
        "personal_records": personal_record
    }

@workoutrouter.get("/workouts/{workout_id}", response_model=WorkoutLogOut )
def get_all_workouts_by_id(workout_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
    ):

    logs = db.query(WorkoutLog).filter(WorkoutLog.id == workout_id, WorkoutLog.user_id == current_user.id).first()

    if not logs:
        raise HTTPException(status_code=404, detail="Workout not found")

    return logs

@workoutrouter.delete("/workouts/{workout_id}", status_code=200)
def delete_workout_by_id(workout_id: int,
                         db: Session = Depends(get_db),
                         current_user = Depends(get_current_user)
                         ):

    log = db.query(WorkoutLog).filter(WorkoutLog.id == workout_id, WorkoutLog.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Workout not found")

    db.delete(log)
    db.commit()

    return  {"message": "Workout deleted successfully"}

