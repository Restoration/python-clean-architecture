from fastapi import FastAPI
from factory.user import UserFactory
from presentation.dto.user import CreateUserRequest

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {}

@app.get("/user/hello_world")
def hello_world():
    return UserFactory.controller().hello_world()

@app.post("/user")
def create_user(request: CreateUserRequest):
    return UserFactory.controller().create_user(request)
