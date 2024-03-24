from interface.repository.user import UserRepositoryInterface

class UserUsecaseInterface(userRepository = UserRepositoryInterface):
    def hello_world(self) -> str:
        pass