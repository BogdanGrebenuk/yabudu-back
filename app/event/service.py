from asyncio import gather

import aiohttp


class GlobalEventsFinder:

    def __init__(self, tm_api_url, tm_api_key):
        self._tm_api_url = tm_api_url
        self._tm_api_key = tm_api_key

    async def find_events(self):
        raw_events_data = await self._make_api_call()
        normalized_events = self._normalize_events(raw_events_data)
        return normalized_events

    async def _make_api_call(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self._tm_api_url,
                    params={
                        'apikey': self._tm_api_key
                    }
            ) as resp:
                return await resp.json()

    def _normalize_events(self, raw_events_data):
        actual_events_data = raw_events_data.get('_embedded', {}).get('events')
        if actual_events_data is None:
            return []

        temp = []
        for event_data in actual_events_data:
            temp.append({
                'name': event_data.get('name'),
                'url': event_data.get('url'),
                # 'start_at': event_data.get('dates', {}).get('dateTime'),
                # 'city': event_data.get('_embedded', {}).get('venues', {}).get('city', {}).get('name'),
                # 'country': event_data.get('_embedded', {}).get('venues', {}).get('country', {}).get('name')
            })

        return temp


class EventInfoGenerator:

    def __init__(self, participation_mapper):
        self.participation_mapper = participation_mapper

    async def generate(self, event):
        organizer_info = await self.participation_mapper.get_event_organizer(event)
        other_participators_info = await self.participation_mapper.find_event_members(event)

        return {
            "id": event.id,
            "name": event.name,
            "description": event.name,
            "startAt": event.start_at.timestamp(),
            "endAt": event.end_at.timestamp(),
            "x": event.x,
            "y": event.y,
            "address": event.address,
            "interests": event.interests,
            "image": event.image,
            "organizer": {
                "id": organizer_info.id,
                "username": organizer_info.username,
                "email": organizer_info.email,
                "instUsername": organizer_info.inst_username,
                "isOrganizer": organizer_info.role,
                "exposeMyData": organizer_info.type
            },
            "members": [
                {
                    "id": member.id,
                    "username": member.username,
                    "email": member.email,
                    "instUsername": member.inst_username,
                    "isOrganizer": member.role,
                    "exposeMyData": member.type
                }
                for member in other_participators_info
            ]
        }

    async def generate_many(self, events):
        return await gather(*[
            self.generate(event)
            for event in events
        ])
