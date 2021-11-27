from dataclasses import dataclass


@dataclass
class CreateUserDto:
    id: str
    username: str
    email: str
    password: str
    inst_username: str


@dataclass
class AuthenticateUserDto:
    email: str
    password: str
