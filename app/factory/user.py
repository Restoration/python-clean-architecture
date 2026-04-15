from presentation.controller.user import UserController
from application.interactor.user import UserInteractor
from infrastructure.repository.user import UserRepository


class UserFactory:
    @staticmethod
    def controller():
        return UserController(UserFactory.usecase())

    @staticmethod
    def usecase():
        return UserInteractor(UserFactory.repository())

    @staticmethod
    def repository():
        return UserRepository()
