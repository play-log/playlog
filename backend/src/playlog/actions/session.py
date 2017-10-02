from uuid import uuid4


KEY = 'playlog:session'
LIFETIME = 86400  # TODO: get from config


async def create(redis):
    sid = uuid4().hex
    await redis.setex(KEY, LIFETIME, sid)
    return sid


async def get(redis):
    sid = await redis.get(KEY)
    if sid:
        sid = sid.decode('utf-8')
    return sid


async def verify(redis, sid):
    current_sid = await get(redis)
    return current_sid and (current_sid == sid)
