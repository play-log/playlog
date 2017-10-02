import json


KEY = 'playlog:nowplay'


async def set_track(redis, artist, album, title, length):
    await redis.setex(KEY, length, json.dumps({
        'artist': artist,
        'album': album,
        'title': title
    }))


async def get_track(redis):
    data = await redis.get(KEY)
    if data:
        return json.loads(data.decode('utf-8'))
