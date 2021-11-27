from dataclasses import dataclass


@dataclass
class CreateUserDto:
    id: str
    username: str
    email: str
    password: str
    inst_username: str
    interests: list


@dataclass
class AuthenticateUserDto:
    email: str
    password: str
