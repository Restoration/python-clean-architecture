from abc import ABC, abstractmethod
from domain.user import User, UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def request(self) -> User:
        pass

    @abstractmethod
    def create_user(self, name: str, email: str, age: int) -> UserEntity:
        pass
