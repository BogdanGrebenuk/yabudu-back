from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.chat.controllers import post_message, get_messages
from app.chat.transformer import MessageTransformer


class ChatPackageContainer(containers.DeclarativeContainer):

    mappers = providers.DependenciesContainer()

    # services

    message_transformer = providers.Factory(
        MessageTransformer,
        user_mapper=mappers.user_mapper
    )

    # controllers

    post_message = ext_aiohttp.View(
        post_message,
        event_mapper=mappers.event_mapper,
        message_mapper=mappers.message_mapper,
        message_transformer=message_transformer
    )

    get_messages = ext_aiohttp.View(
        get_messages,
        event_mapper=mappers.event_mapper,
        message_mapper=mappers.message_mapper,
        message_transformer=message_transformer
    )
