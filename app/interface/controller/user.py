from abc import ABC, abstractmethod

from presentation.dto.user import GetUserDTO, CreateUserRequest, CreateUserResponse


class IUserController(ABC):
    @abstractmethod
    def hello_world(self) -> GetUserDTO:
        pass

    @abstractmethod
    def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        pass
