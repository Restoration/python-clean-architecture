from pydantic import BaseModel


class GetUserDTO(BaseModel):
    message: str
