from interface.usecase.user import UserUsecaseInterface
from interface.repository.user import UserRepositoryInterface

class UserUsecase(UserUsecaseInterface):
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def hello_world(self) -> str:
        user = self.repo.request()
        return user.message
