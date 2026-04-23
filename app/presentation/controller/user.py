from interface.controller.user import IUserController
from interface.usecase.user import IUserUsecase
from presentation.dto.user import GetUserDTO


class UserController(IUserController):
    def __init__(self, usecase: IUserUsecase) -> None:
        self.uc = usecase

    def hello_world(self) -> GetUserDTO:
        return GetUserDTO(
            message=self.uc.hello_world()
        )
