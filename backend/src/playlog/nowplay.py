import json


class Nowplay(object):
    KEY = 'playlog:nowplay'

    def __init__(self, redis):
        self.redis = redis

    async def set(self, artist, album, title, length):
        await self.redis.setex(self.KEY, length, json.dumps({
            'artist': artist,
            'album': album,
            'title': title
        }))

    async def get(self):
        data = await self.redis.get(self.KEY)
        if data:
            return json.loads(data)
