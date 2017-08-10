from uuid import uuid4

DEFAULT_LIFETIME = 86400


class Session(object):
    KEY = 'playlog:session'

    def __init__(self, redis):
        self.redis = redis
        self.lifetime = DEFAULT_LIFETIME

    async def create(self):
        session_id = uuid4().hex
        await self.redis.setex(self.KEY, self.lifetime, session_id)
        return session_id

    async def get(self):
        session_id = await self.redis.get(self.KEY)
        if session_id:
            session_id = session_id.decode('utf-8')
        return session_id

    async def verify(self, session_id):
        current_session = await self.get()
        return current_session and (current_session == session_id)
