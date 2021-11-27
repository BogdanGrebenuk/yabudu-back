import uuid
from datetime import datetime

from aiohttp import web

from app.event.domain import Event, Participation


async def get_global_events(request, global_events_finder):
    global_events = await global_events_finder.find_events()
    return web.json_response(global_events, status=200)


async def create_event(request, event_mapper, participation_mapper, event_transformer):
    body = await request.json()
    user = request['user']

    event = Event(
        id=str(uuid.uuid4()),
        name=body.get('name'),
        description=body.get('description'),
        start_at=datetime.fromtimestamp(body.get('start_at')),
        end_at=datetime.fromtimestamp(body.get('end_at')),
        x=body.get('x'),
        y=body.get('y'),
        address=body.get('address'),
        interests=body.get('interests')
    )

    await event_mapper.create(event)

    participation = Participation(
        id=str(uuid.uuid4()),
        user_id=user.id,
        event_id=event.id,
        type=body.get('type'),
        role=True,
    )

    await participation_mapper.create(participation)

    return web.json_response(await event_transformer.transform(event))
