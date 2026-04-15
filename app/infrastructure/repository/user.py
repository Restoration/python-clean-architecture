from interface.repository.user import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def request(self) -> str:
        return "hello world"