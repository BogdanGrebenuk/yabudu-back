import uuid
from datetime import datetime

from aiohttp import web

from app.event.domain import Event, Participation


async def get_global_events(request, global_events_finder):
    global_events = await global_events_finder.find_events()
    return web.json_response(global_events, status=200)


async def create_event(request, event_mapper, participation_mapper, event_transformer, event_info_generator):
    body = await request.json()
    user = request['user']

    event = Event(
        id=str(uuid.uuid4()),
        name=body.get('name'),
        description=body.get('description'),
        start_at=datetime.utcfromtimestamp(body.get('startAt')),
        end_at=datetime.utcfromtimestamp(body.get('endAt')),
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

    event_info = await event_info_generator.generate(event)

    return web.json_response(await event_transformer.transform(event_info))


async def get_event(request, event_mapper, event_transformer, event_info_generator):
    user = request['user']
    event_id = request.match_info.get('event_id')
    event = await event_mapper.find(
        id=event_id
    )

    event_info = await event_info_generator.generate(event)

    return web.json_response(await event_transformer.transform(event_info))


async def get_my_events(request, event_mapper, event_transformer, event_info_generator):
    user = request['user']

    events = await event_mapper.find_events_with_user_participation(user)

    events_info = await event_info_generator.generate_many(events)

    return web.json_response(await event_transformer.transform(events_info))


async def get_all_events(request, event_mapper, event_transformer, event_info_generator):
    user = request['user']
    events = await event_mapper.find_all()
    user_events_ids = [event.id for event in await event_mapper.find_events_with_user_participation(user)]

    events_without_user_participation_that_not_finished_yet = [
        event
        for event in events
        if event.id not in user_events_ids and datetime.utcnow().timestamp() < event.end_at.timestamp()
    ]

    events_info = await event_info_generator.generate_many(events_without_user_participation_that_not_finished_yet)

    return web.json_response(
        await event_transformer.transform(events_info)
    )


async def join_to_event(request, event_mapper, participation_mapper, event_transformer, event_info_generator):
    user = request['user']
    body = await request.json()
    event_id = request.match_info.get('event_id')

    participation = Participation(
        id=str(uuid.uuid4()),
        user_id=user.id,
        event_id=event_id,
        type=body.get('type'),
        role=False,
    )

    event = await event_mapper.find(
        id=event_id
    )

    await participation_mapper.create(participation)

    event_info = await event_info_generator.generate(event)

    return web.json_response(await event_transformer.transform(event_info))
