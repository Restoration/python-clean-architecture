from typing import Dict
from interface.controller.user import IUserController
from interface.usecase.user import IUserUsecase

class UserController(IUserController):
    def __init__(self, usecase: IUserUsecase) -> None:
        self.uc = usecase

    def hello_world(self) -> Dict[str, str]:
        return {
            "say": self.uc.hello_world()
        }
