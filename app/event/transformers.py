from asyncio import gather

from app.utils.transformer import Transformer


class EventTransformer(Transformer):

    def __init__(self, participation_mapper):
        self.participation_mapper = participation_mapper

    async def transform(self, data):
        return data

    async def transform_with_user_info(self, event, user):
        participation = await self.participation_mapper.find_one_by(event_id=event.id, user_id=user.id)
        return await self.transform({
            "id": event.id,
            "name": event.name,
            "description": event.name,
            "startAt": event.start_at.timestamp(),
            "endAt": event.end_at.timestamp(),
            "x": event.x,
            "y": event.y,
            "address": event.address,
            "interests": event.interests,
            "isCreator": participation.role,
            "exposeMyData": participation.type,
            "image": event.image
        })

    async def transform_many_with_user_info(self, events, user):
        return await gather(*[
            self.transform_with_user_info(event, user)
            for event in events
        ])

    async def transform_without_user_info(self, event):
        return await self.transform({
            "id": event.id,
            "name": event.name,
            "description": event.name,
            "startAt": event.start_at.timestamp(),
            "endAt": event.end_at.timestamp(),
            "x": event.x,
            "y": event.y,
            "address": event.address,
            "interests": event.interests,
            "image": event.image
        })

    async def transform_many_without_user_info(self, events):
        return await gather(*[
            self.transform_without_user_info(event)
            for event in events
        ])
