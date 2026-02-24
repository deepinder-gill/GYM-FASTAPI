from fastapi import FastAPI
from app.routes.user_routes import router
from app.database import engine, Base
from app.models.models import User
from app.routes.workout_route import workoutrouter

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)

app.include_router(workoutrouter)





