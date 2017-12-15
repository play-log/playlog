from uuid import uuid4

from playlog.config import SESSION_LIFETIME


KEY = 'playlog:session'


async def create(redis):
    sid = uuid4().hex
    await redis.execute('setex', KEY, SESSION_LIFETIME, sid)
    return sid


async def get(redis):
    sid = await redis.execute('get', KEY)
    if sid:
        sid = sid.decode('utf-8')
    return sid


async def verify(redis, sid):
    current_sid = await get(redis)
    return current_sid and (current_sid == sid)
