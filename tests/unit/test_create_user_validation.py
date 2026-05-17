import pytest
from pydantic import ValidationError

from presentation.dto.user import CreateUserRequest


class TestCreateUserRequestValidation:
    def test_valid_request(self):
        req = CreateUserRequest(name="Taro", email="taro@example.com", age=25)
        assert req.name == "Taro"
        assert req.email == "taro@example.com"
        assert req.age == 25

    def test_name_stripped(self):
        req = CreateUserRequest(name="  Taro  ", email="taro@example.com", age=25)
        assert req.name == "Taro"

    def test_name_blank_rejected(self):
        with pytest.raises(ValidationError):
            CreateUserRequest(name="   ", email="taro@example.com", age=25)

    def test_name_empty_rejected(self):
        with pytest.raises(ValidationError):
            CreateUserRequest(name="", email="taro@example.com", age=25)

    def test_name_too_long_rejected(self):
        with pytest.raises(ValidationError):
            CreateUserRequest(name="a" * 101, email="taro@example.com", age=25)

    def test_invalid_email_rejected(self):
        with pytest.raises(ValidationError):
            CreateUserRequest(name="Taro", email="not-an-email", age=25)

    def test_negative_age_rejected(self):
        with pytest.raises(ValidationError):
            CreateUserRequest(name="Taro", email="taro@example.com", age=-1)

    def test_age_over_150_rejected(self):
        with pytest.raises(ValidationError):
            CreateUserRequest(name="Taro", email="taro@example.com", age=151)

    def test_age_zero_accepted(self):
        req = CreateUserRequest(name="Baby", email="baby@example.com", age=0)
        assert req.age == 0

    def test_age_150_accepted(self):
        req = CreateUserRequest(name="Elder", email="elder@example.com", age=150)
        assert req.age == 150
