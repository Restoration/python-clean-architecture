from interface.usecase.user import IUserInteractor
from interface.repository.user import IUserRepository

class UserInteractor(IUserInteractor):
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    def hello_world(self) -> str:
        user = self.repo.request()
        return user.message
