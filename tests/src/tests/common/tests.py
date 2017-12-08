import os
import sys

from requests import get, post

from playlog import config
from playlog.lib.json import Encoder

from tests import TestCase


class TestConfig(TestCase):
    def test_getenv(self):
        with self.assertRaises(KeyError) as ctx:
            config.getenv('unknown')
        self.assertEqual(ctx.exception.args, (
            'Environment variable "PLAYLOG_UNKNOWN" is not set',
        ))
        self.assertIsNone(config.getenv('unknown', required=False))
        os.environ['PLAYLOG_UNKNOWN'] = ''
        try:
            with self.assertRaises(ValueError) as ctx:
                config.getenv('unknown')
            self.assertEqual(ctx.exception.args, (
                'Environment variable "PLAYLOG_UNKNOWN" can not be empty',
            ))
        finally:
            os.environ.pop('PLAYLOG_UNKNOWN')

    def test_debug_not_valid(self):
        old_value = os.environ['PLAYLOG_DEBUG']
        os.environ['PLAYLOG_DEBUG'] = 'x'
        sys.modules.pop('playlog.config')
        try:
            with self.assertRaises(ValueError) as ctx:
                import playlog.config   # noqa
            self.assertEqual(ctx.exception.args, (
                'Unexpected "DEBUG" value: expects "false" or "true", "x" given',
            ))
        finally:
            os.environ['PLAYLOG_DEBUG'] = old_value


class TestJSON(TestCase):
    def test_encoder(self):
        encoder = Encoder()
        with self.assertRaises(TypeError):
            encoder.default(object())


class TestResponseMiddleware(TestCase):
    def test_unknown_accept_header(self):
        rep = get(self.url('overview'), headers={'Accept': 'text/xml'})
        self.assertEqual(rep.status_code, 400, rep.text)
