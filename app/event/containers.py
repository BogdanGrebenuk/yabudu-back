from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.event.controllers import get_global_events, create_event, get_event, join_to_event, get_my_events, get_all_events
from app.event.service import GlobalEventsFinder
from app.event.transformers import EventTransformer


class EventPackageContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    mappers = providers.DependenciesContainer()

    event_transformer = providers.Singleton(
        EventTransformer,
        participation_mapper=mappers.participation_mapper
    )

    # services

    global_events_finder = providers.Factory(
        GlobalEventsFinder,
        tm_api_url=config.tm.api_url,
        tm_api_key=config.tm.api_key
    )

    # controllers

    get_global_events = ext_aiohttp.View(
        get_global_events,
        global_events_finder=global_events_finder,
    )

    create_event = ext_aiohttp.View(
        create_event,
        event_mapper=mappers.event_mapper,
        participation_mapper=mappers.participation_mapper,
        event_transformer=event_transformer,
    )

    get_event_by_id = ext_aiohttp.View(
        get_event,
        event_mapper=mappers.event_mapper,
        event_transformer=event_transformer,
    )

    join_to_event = ext_aiohttp.View(
        join_to_event,
        event_mapper=mappers.event_mapper,
        participation_mapper=mappers.participation_mapper,
        event_transformer=event_transformer,
    )

    get_my_events = ext_aiohttp.View(
        get_my_events,
        event_transformer=event_transformer,
        event_mapper=mappers.event_mapper,
    )

    get_all_events = ext_aiohttp.View(
        get_all_events,
        event_transformer=event_transformer,
        event_mapper=mappers.event_mapper,
    )
