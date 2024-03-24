from abc import ABC, abstractmethod
from interface.repository.user import UserRepositoryInterface

class UserUsecaseInterface(ABC):
    @abstractmethod
    def __init__(self, repo: UserRepositoryInterface) -> None:
        pass
    @abstractmethod
    def hello_world(self) -> str:
        pass