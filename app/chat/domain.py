import dataclasses
import datetime

from app.utils.mapper import Entity


@dataclasses.dataclass
class Message(Entity):
    id: str
    text: str
    event_id: str
    user_id: str
    created_at: datetime.datetime
