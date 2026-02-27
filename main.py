from fastapi import FastAPI
from routes.user_routes import router
from database import engine, Base
from models.models import User
from routes.workout_route import workoutrouter

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)

app.include_router(workoutrouter)

