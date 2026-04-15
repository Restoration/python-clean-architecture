from abc import ABC, abstractmethod
from domain.user.entity import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def request(self) -> User:
        pass