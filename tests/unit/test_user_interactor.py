from domain.user import User
from interface.repository.user import IUserRepository
from application.interactor.user import UserInteractor


class FakeUserRepository(IUserRepository):
    def __init__(self, user: User) -> None:
        self._user = user

    def request(self) -> User:
        return self._user


class TestUserInteractor:
    def test_hello_world_returns_message(self):
        repo = FakeUserRepository(User(message="hello world"))
        interactor = UserInteractor(repo)

        result = interactor.hello_world()

        assert result == "hello world"

    def test_hello_world_returns_custom_message(self):
        repo = FakeUserRepository(User(message="custom message"))
        interactor = UserInteractor(repo)

        result = interactor.hello_world()

        assert result == "custom message"
