import os
import sys

import pytest

from playlog import config


def test_getenv():
    with pytest.raises(KeyError):
        config.getenv('unknown')
    assert config.getenv('unknown', required=False) is None

    os.environ['PLAYLOG_UNKNOWN'] = ''
    try:
        with pytest.raises(ValueError):
            config.getenv('unknown')
    finally:
        os.environ.pop('PLAYLOG_UNKNOWN')


def test_debug_not_valid():
    old_value = os.environ['PLAYLOG_DEBUG']
    os.environ['PLAYLOG_DEBUG'] = 'x'
    sys.modules.pop('playlog.config')
    try:
        with pytest.raises(ValueError):
            import playlog.config   # noqa
    finally:
        os.environ['PLAYLOG_DEBUG'] = old_value
