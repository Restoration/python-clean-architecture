from abc import ABC, abstractmethod

from domain.user import UserEntity


class IUserUsecase(ABC):
    @abstractmethod
    def hello_world(self) -> str:
        pass

    @abstractmethod
    def create_user(self, name: str, email: str, age: int) -> UserEntity:
        pass