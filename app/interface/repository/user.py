from abc import ABC, abstractmethod
class UserRepositoryInterface(ABC):
    @abstractmethod
    def request(self) -> str:
        pass