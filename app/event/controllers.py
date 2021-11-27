from aiohttp import web


async def get_global_events(request, global_events_finder):
    global_events = await global_events_finder.find_events()
    return web.json_response(global_events, status=200)
