from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
