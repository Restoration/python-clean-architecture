from interface.repository.user import UserRepositoryInterface

class UserUsecase: 
    def __init__(self, repo: UserRepositoryInterface) -> None:
        self.repo = repo

    def hello_world(self) -> str:
        return self.repo.request()
