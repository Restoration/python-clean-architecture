from typing import Dict
from interface.handler.user import IUserHandler
from interface.usecase.user import IUserUsecase

class UserHandler(IUserHandler):
    def __init__(self, usecase: IUserUsecase) -> None:
        self.uc = usecase

    def hello_world(self) -> Dict[str, str]:
        return {
            "say": self.uc.hello_world()
        }