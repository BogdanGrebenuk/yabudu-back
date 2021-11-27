import datetime
import uuid

from aiohttp import web

from app.chat.domain import Message


async def post_message(
        request,
        event_mapper,
        message_mapper,
        message_transformer
        ):
    event_id = request.match_info.get('event_id')
    body = await request.json()

    event = await event_mapper.find(event_id)
    user = request['user']

    message = Message(
        id=str(uuid.uuid4()),
        text=body.get('text'),
        event_id=event.id,
        user_id=user.id,
        created_at=datetime.datetime.utcnow()
    )

    await message_mapper.create(message)

    messages = await message_mapper.find_by(event_id=event.id)

    messages.sort(key=lambda m: m.created_at)

    return web.json_response(
        await message_transformer.transform_many(messages),
        status=201
    )


async def get_messages(
        request,
        event_mapper,
        message_mapper,
        message_transformer
        ):
    event_id = request.match_info.get('event_id')

    event = await event_mapper.find(event_id)

    messages = await message_mapper.find_by(event_id=event.id)

    messages.sort(key=lambda m: m.created_at)

    return web.json_response(
        await message_transformer.transform_many(messages),
        status=200
    )
