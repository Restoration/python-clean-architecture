from dataclasses import dataclass


@dataclass
class User:
    message: str


@dataclass
class UserEntity:
    name: str
    email: str
    age: int
