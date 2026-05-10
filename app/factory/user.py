from interface.controller.user import IUserController
from interface.usecase.user import IUserUsecase
from interface.repository.user import IUserRepository
from presentation.controller.user import UserController
from application.interactor.user import UserInteractor
from infrastructure.repository.user import UserRepository


class UserFactory:
    @staticmethod
    def controller() -> IUserController:
        return UserController(UserFactory.usecase())

    @staticmethod
    def usecase() -> IUserUsecase:
        return UserInteractor(UserFactory.repository())

    @staticmethod
    def repository() -> IUserRepository:
        return UserRepository()
