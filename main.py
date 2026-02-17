from fastapi import FastAPI
from app.routes import user_routes
app = FastAPI()


app.include_router(user_routes.router)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
