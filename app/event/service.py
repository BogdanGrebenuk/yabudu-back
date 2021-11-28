from asyncio import gather
from datetime import datetime

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
                    self._tm_api_url + '?size=5',
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
                'startAt': event_data.get('dates', {}).get('start', {}).get('dateTime'),
                'city': event_data.get('_embedded', {}).get('venues', [{}])[0].get('city', {}).get('name'),
                'country': event_data.get('_embedded', {}).get('venues', [{}])[0].get('country', {}).get('name'),
            })

        return temp


class EventInfoGenerator:

    def __init__(self, participation_mapper, feedback_mapper):
        self.participation_mapper = participation_mapper
        self.feedback_mapper = feedback_mapper

    async def generate(self, event):
        organizer_info = await self.participation_mapper.get_event_organizer(event)
        other_participators_info = await self.participation_mapper.find_event_members(event)

        if datetime.utcnow().timestamp() > event.end_at.timestamp():
            raw_feedbacks = await self.feedback_mapper.find_by(event_id=event.id)
            feedbacks = [
                {
                    "image": feedback.image,
                    "text": feedback.text,
                    "userId": feedback.user_id,
                    "username": (
                        organizer_info.username
                        if organizer_info.id == feedback.user_id
                        else
                            [p.username for p in other_participators_info if p.user_id == feedback.user_id][0]
                    )
                }
                for feedback in raw_feedbacks
            ]
        else:
            feedbacks = []

        return {
            "id": event.id,
            "name": event.name,
            "description": event.name,
            "startAt": event.start_at.timestamp(),
            "endAt": event.end_at.timestamp(),
            "isOver": datetime.utcnow().timestamp() > event.end_at.timestamp(),
            "x": event.x,
            "y": event.y,
            "address": event.address,
            "interests": event.interests,
            "image": event.image,
            "feedbacks": feedbacks,
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


class EventSuggester:

    def __init__(self, logger):
        self.logger = logger

    async def sort_events_by_suggested_interests(self, user, events):
        try:
            suggested_interests = (await self._make_api_call(user.interests)).get('suggestedInterests')
            event_map = {event.id: event for event in events}
            temp = {}
            for event in events:
                temp[event.id] = 0
                for interest in event.interests:
                    if interest in suggested_interests:
                        temp[event.id] += 1
            event_ids = [
                item[0]
                for item in sorted(temp.items(), key=lambda item: item[1], reverse=True)
            ]
            self.logger.info(f"Prediction successfully made: {suggested_interests}, {temp}, {event_ids}")
            return [
                event_map[event_id]
                for event_id in event_ids
            ]
        except Exception as e:
            self.logger.exception(e)
            return events

    async def _make_api_call(self, interests):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    'http://207.154.228.5:8000/api/predict-interests',
                    json={
                        'interests': interests
                    }
            ) as resp:
                return await resp.json()
