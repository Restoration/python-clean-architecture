from interface.usecase.user import IUserUsecase
from presentation.controller.user import UserController
from presentation.dto.user import GetUserDTO


class FakeUserUsecase(IUserUsecase):
    def __init__(self, message: str) -> None:
        self._message = message

    def hello_world(self) -> str:
        return self._message


class TestUserController:
    def test_hello_world_returns_dto(self):
        usecase = FakeUserUsecase("hello world")
        controller = UserController(usecase)

        result = controller.hello_world()

        assert isinstance(result, GetUserDTO)

    def test_hello_world_returns_correct_message(self):
        usecase = FakeUserUsecase("hello world")
        controller = UserController(usecase)

        result = controller.hello_world()

        assert result.message == "hello world"

    def test_hello_world_returns_custom_message(self):
        usecase = FakeUserUsecase("custom message")
        controller = UserController(usecase)

        result = controller.hello_world()

        assert result.message == "custom message"
