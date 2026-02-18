from fastapi import FastAPI
from app.routes.user_routes import router
from app.database import engine, Base
from app.models.models import User


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(router)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
