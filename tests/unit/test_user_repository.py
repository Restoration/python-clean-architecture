from domain.user import User
from infrastructure.repository.user import UserRepository


class TestUserRepository:
    def test_request_returns_user_entity(self):
        repo = UserRepository()

        result = repo.request()

        assert isinstance(result, User)

    def test_request_returns_hello_world_message(self):
        repo = UserRepository()

        result = repo.request()

        assert result.message == "hello world"
