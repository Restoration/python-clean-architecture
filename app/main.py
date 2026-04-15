from fastapi import FastAPI
from factory.user import UserFactory

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {}

@app.get("/user/hello_world")
def hello_world():
    return UserFactory.handler().hello_world()
