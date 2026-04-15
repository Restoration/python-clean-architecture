from fastapi import FastAPI
from container.user import BuildUserHandler

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {}

@app.get("/user/hello_world")
def hello_world():
    return BuildUserHandler().hello_world()
