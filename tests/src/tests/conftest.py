import json

import pytest

from redis import StrictRedis

from playlog.config import REDIS_URL


@pytest.fixture
def redis():
    conn = StrictRedis(*REDIS_URL)
    try:
        yield conn
    finally:
        conn.flushdb()


@pytest.fixture
def get_session_id(redis):
    def wrapper():
        session_id = redis.get('playlog:session')
        return session_id.decode('utf-8') if session_id else None
    return wrapper


@pytest.fixture
def get_current_track(redis):
    def wrapper():
        data = redis.get('playlog:nowplay')
        return json.loads(data.decode('utf-8')) if data else None
    return wrapper


@pytest.fixture
def set_current_track(redis):
    def wrapper(**kwargs):
        redis.set('playlog:nowplay', json.dumps(kwargs))
    return wrapper
