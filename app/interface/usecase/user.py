from abc import ABC, abstractmethod

class UserUsecaseInterface(ABC):
    @abstractmethod
    def hello_world(self) -> str:
        pass