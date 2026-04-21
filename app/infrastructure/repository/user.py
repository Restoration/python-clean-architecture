from domain.user import User
from interface.repository.user import IUserRepository
from infrastructure.dao.user import UserDao


class UserRepository(IUserRepository):
    def request(self) -> User:
        dao = UserDao(message="hello world")
        return User(message=dao.message)