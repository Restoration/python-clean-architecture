from pydantic import BaseModel, Field, field_validator


class GetUserDTO(BaseModel):
    message: str


class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(..., ge=0, le=150)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("name must not be blank")
        return v.strip()


class CreateUserResponse(BaseModel):
    name: str
    email: str
    age: int
