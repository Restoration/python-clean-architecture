from interface.usecase.user import IUserUsecase
from interface.repository.user import IUserRepository
from domain.user import UserEntity


class UserInteractor(IUserUsecase):
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    def hello_world(self) -> str:
        user = self.repo.request()
        return user.message

    def create_user(self, name: str, email: str, age: int) -> UserEntity:
        return self.repo.create_user(name, email, age)
