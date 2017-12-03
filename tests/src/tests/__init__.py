import inspect
import json

from pathlib import Path
from unittest import TestCase as BaseTestCase
from urllib.parse import urlencode

from redis import StrictRedis

from playlog import config, models

from .alchemy import Alchemy


db = Alchemy(config.SA_URL, models.metadata)
redis = StrictRedis(*config.REDIS_URL)


class TestCase(BaseTestCase):
    BASE_URL = 'http://127.0.0.1:8080'
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        db.setup()

    @classmethod
    def tearDownClass(cls):
        db.teardown()

    def setUp(self):
        filename = '{}.yml'.format(self._testMethodName)
        filepath = Path(inspect.getfile(self.__class__)).parent / 'fixtures' / filename
        if filepath.exists():
            db.load(filepath)

    def tearDown(self):
        db.clean()
        redis.flushdb()

    def url(self, path, **params):
        return '{}/{}?{}'.format(self.BASE_URL, path, urlencode(params))


def get_session_id():
    session_id = redis.get('playlog:session')
    return session_id.decode('utf-8') if session_id else None


def get_current_track():
    data = redis.get('playlog:nowplay')
    return json.loads(data.decode('utf-8')) if data else None


def set_current_track(**kwargs):
    redis.set('playlog:nowplay', json.dumps(kwargs))
