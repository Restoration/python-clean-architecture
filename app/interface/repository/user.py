from abc import ABC, abstractmethod
from domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def request(self) -> User:
        pass
