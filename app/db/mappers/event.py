from sqlalchemy import select

from app.db.models import Participation
from app.utils.mapper import Mapper


class EventMapper(Mapper):

    async def find_events_with_user_participation(self, user):
        async with self.engine.acquire() as conn:
            result = await (
                await conn.execute(
                    select([self.model])
                    .select_from(self.model.join(Participation, self.model.c.id == Participation.c.event_id))
                    .where(Participation.c.user_id == user.id)
                )
            ).fetchall()
            return [self.entity_cls(**i) for i in result]
