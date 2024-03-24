from interface.usecase.user import UserUsecaseInterface

class UserHandler(usecase = UserUsecaseInterface):
    def __init__(self, uc: UserUsecaseInterface) -> None:
        self.uc = uc
    def hello_world(self):
       return self.us.hello_world()