from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.event.controllers import get_global_events
from app.event.service import GlobalEventsFinder


class EventPackageContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

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
