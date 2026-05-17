from interface.controller.user import IUserController
from interface.usecase.user import IUserUsecase
from presentation.dto.user import GetUserDTO, CreateUserRequest, CreateUserResponse


class UserController(IUserController):
    def __init__(self, usecase: IUserUsecase) -> None:
        self.uc = usecase

    def hello_world(self) -> GetUserDTO:
        return GetUserDTO(
            message=self.uc.hello_world()
        )

    def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        user = self.uc.create_user(
            name=request.name,
            email=request.email,
            age=request.age,
        )
        return CreateUserResponse(
            name=user.name,
            email=user.email,
            age=user.age,
        )
