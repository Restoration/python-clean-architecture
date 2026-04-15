from presentation.handler.user import UserHandler
from application.interactor.user import UserUsecase
from infrastructure.repository.user import UserRepository

def BuildUserHandler():
    return UserHandler(
        BuildUserUseCase()
    )

def BuildUserUseCase():
    return UserUsecase(
        BuildUserRepository()
    )

def BuildUserRepository():
    return UserRepository()
    