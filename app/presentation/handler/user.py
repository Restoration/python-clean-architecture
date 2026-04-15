from typing import Dict
from interface.handler.user import UserHandlerInterface
from interface.usecase.user import UserUsecaseInterface

class UserHandler(UserHandlerInterface):
    def __init__(self, usecase: UserUsecaseInterface) -> None:
        self.uc = usecase

    def hello_world(self) -> Dict[str, str]:
        return {
            "say": self.uc.hello_world()
        }