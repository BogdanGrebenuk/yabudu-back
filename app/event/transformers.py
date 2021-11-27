from app.utils.transformer import Transformer


class EventTransformer(Transformer):

    async def transform(self, event):
        return {
            "id": event.id,
            "name": event.name,
            "description": event.name,
            "start_at": event.start_at.timestamp(),
            "end_at": event.end_at.timestamp(),
            "x": event.x,
            "y": event.y,
            "address": event.address,
            "interests": event.interests,
        }
