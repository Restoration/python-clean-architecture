from presentation.handler.user import UserHandler
from application.interactor.user import UserUsecase
from infrastructure.repository.user import UserRepository

def build_user_handler():
    return UserHandler(
        build_user_usecase()
    )

def build_user_usecase():
    return UserUsecase(
        build_user_repository()
    )

def build_user_repository():
    return UserRepository()
