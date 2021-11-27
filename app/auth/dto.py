from dataclasses import dataclass


@dataclass
class CreateUserDto:
    id: str
    username: str
    email: str
    password: str


@dataclass
class AuthenticateUserDto:
    email: str
    password: str
