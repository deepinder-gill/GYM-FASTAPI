from fastapi import FastAPI
from app.routes.user_routes import router
from app.database import engine, Base
from app.models.models import User
from app.routes.workout import workoutrouter

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router, workoutrouter)



