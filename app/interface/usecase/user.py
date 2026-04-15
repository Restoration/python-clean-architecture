from abc import ABC, abstractmethod

class IUserUsecase(ABC):
    @abstractmethod
    def hello_world(self) -> str:
        pass