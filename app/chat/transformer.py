from app.utils.transformer import Transformer


class MessageTransformer(Transformer):

    def __init__(self, user_mapper):
        self.user_mapper = user_mapper

    async def transform(self, message):
        return {
            'id': message.id,
            'text': message.text,
            'event_id': message.event_id,
            'user_id': message.user_id,
            'username': (await self.user_mapper.find(message.user_id)).username,
            'created_at': message.created_at.timestamp()
        }
