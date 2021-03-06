from dataclasses import dataclass
from datetime import datetime

from app.utils.mapper import Entity


@dataclass
class Event(Entity):
    id: str
    name: str
    description: str
    start_at: datetime
    end_at: datetime
    address: str
    interests: list
    x: float
    y: float
    image: str


@dataclass
class Participation(Entity):
    id: str
    user_id: str
    event_id: str
    type: bool
    role: bool


@dataclass
class Feedback(Entity):
    id: str
    user_id: str
    event_id: str
    text: str
    image: str

