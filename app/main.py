from fastapi import FastAPI
from container.user import build_user_handler

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {}

@app.get("/user/hello_world")
def hello_world():
    return build_user_handler().hello_world()
