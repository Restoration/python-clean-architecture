from abc import ABC, abstractmethod

from presentation.dto.user import GetUserDTO


class IUserController(ABC):
    @abstractmethod
    def hello_world(self) -> GetUserDTO:
        pass
