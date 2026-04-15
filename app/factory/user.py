from presentation.handler.user import UserHandler
from application.interactor.user import UserUsecase
from infrastructure.repository.user import UserRepository


class UserFactory:
    @staticmethod
    def handler():
        return UserHandler(UserFactory.usecase())

    @staticmethod
    def usecase():
        return UserUsecase(UserFactory.repository())

    @staticmethod
    def repository():
        return UserRepository()
