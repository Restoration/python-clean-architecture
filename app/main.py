from fastapi import FastAPI
from container.user import BuildUserHandler

app = FastAPI()


@app.get("/user/hello_world")
def read_root():
    return BuildUserHandler().hello_world()
