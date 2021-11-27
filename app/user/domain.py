from dataclasses import dataclass
from enum import Enum

from app.utils.mapper import Entity


@dataclass
class User(Entity):
    id: str
    username: str
    email: str
    inst_username: str
    password: str
    token: str = None


class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'

    @classmethod
    def get_roles(cls):
        return [i.value for i in cls]
