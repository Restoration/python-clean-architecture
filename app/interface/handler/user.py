from abc import ABC, abstractmethod
from typing import Dict

class UserHandlerInterface(ABC):
    @abstractmethod
    def hello_world(self) -> Dict[str, str]:
        pass