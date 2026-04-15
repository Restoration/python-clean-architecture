from domain.user.entity import User
from interface.repository.user import UserRepositoryInterface
from infrastructure.dto.user import UserDto


class UserRepository(UserRepositoryInterface):
    def request(self) -> User:
        dto = UserDto(message="hello world")
        return User(message=dto.message)