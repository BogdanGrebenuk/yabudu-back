from sqlalchemy import select

from app.db.models import User
from app.utils.mapper import Mapper


class ParticipationMapper(Mapper):

    async def get_event_organizer(self, event):
        async with self.engine.acquire() as conn:
            result = await (
                await conn.execute(
                    select([
                        self.model.role,
                        self.model.type,
                        User.c.id,
                        User.c.username,
                        User.c.email,
                        User.c.inst_username,
                        User.c.interests
                    ])
                    .select_from(self.model.join(User, self.model.c.user_id == User.c.id))
                    .where(self.model.c.event_id == event.id, self.model.c.role == True)
                )
            ).fetchone()
            return result

    async def find_event_members(self, event):
        async with self.engine.acquire() as conn:
            result = await (
                await conn.execute(
                    select([
                        User.c.id,
                        User.c.username,
                        User.c.email,
                        User.c.inst_username,
                        User.c.interests,
                        self.model.role,
                        self.model.type
                    ])
                        .select_from(self.model.join(User, self.model.c.user_id == User.c.id))
                        .where(self.model.c.event_id == event.id, self.model.c.role == False)
                )
            ).fetchall()
            return result
