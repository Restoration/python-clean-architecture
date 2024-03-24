from abc import ABC, abstractmethod
from interface.usecase.user import UserUsecaseInterface

class UserHanlderInterface(ABC):
    @abstractmethod
    def __init__(self, usecase: UserUsecaseInterface) -> None:
        pass

    @abstractmethod
    def hello_world(self) -> str:
        pass