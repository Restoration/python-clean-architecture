from presentation.handler.user import UserHandler
from application.usecase.user import UserUsecase
from infrastructure.respository.user import UserRepository

userHandler = UserHandler()
userUsecase = UserUsecase()
userRepository = UserRepository()

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
    