from interface.usecase.user import IUserUsecase
from interface.repository.user import IUserRepository

class UserInteractor(IUserUsecase):
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    def hello_world(self) -> str:
        user = self.repo.request()
        return user.message
