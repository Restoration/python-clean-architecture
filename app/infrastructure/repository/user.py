from domain.user import User
from interface.repository.user import IUserRepository
from infrastructure.dto.user import UserDto


class UserRepository(IUserRepository):
    def request(self) -> User:
        dto = UserDto(message="hello world")
        return User(message=dto.message)