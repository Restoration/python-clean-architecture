from presentation.handler.user import UserHandler
from application.interactor.user import UserInteractor
from infrastructure.repository.user import UserRepository


class UserFactory:
    @staticmethod
    def handler():
        return UserHandler(UserFactory.usecase())

    @staticmethod
    def usecase():
        return UserInteractor(UserFactory.repository())

    @staticmethod
    def repository():
        return UserRepository()
