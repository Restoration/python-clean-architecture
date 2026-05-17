from domain.user import User, UserEntity
from interface.repository.user import IUserRepository
from infrastructure.dao.user import UserDao


class UserRepository(IUserRepository):
    def request(self) -> User:
        dao = UserDao(message="hello world")
        return User(message=dao.message)

    def create_user(self, name: str, email: str, age: int) -> UserEntity:
        # TODO: 実際のDB保存処理に置き換える
        return UserEntity(name=name, email=email, age=age)