import pytest

from tests.client import get
from tests.fixtures import fixture


def get_count(expected_status=200, **params):
    return get('plays/count', expected_status=expected_status, **params)


@fixture('plays')
@pytest.mark.parametrize('params,data', [
    # Defaults
    ({}, [
        {'label': '2012-01-01T00:00:00', 'value': 1},
        {'label': '2016-01-01T00:00:00', 'value': 1},
        {'label': '2017-01-01T00:00:00', 'value': 31}
    ]),
    # Empty period
    ({'period': ''}, [
        {'label': '2012-01-01T00:00:00', 'value': 1},
        {'label': '2016-01-01T00:00:00', 'value': 1},
        {'label': '2017-01-01T00:00:00', 'value': 31}
    ]),
    # Month
    ({'period': 2017}, [
        {'label': '2017-02-01T00:00:00', 'value': 1},
        {'label': '2017-03-01T00:00:00', 'value': 12},
        {'label': '2017-05-01T00:00:00', 'value': 1},
        {'label': '2017-08-01T00:00:00', 'value': 17}
    ]),
    # Day
    ({'period': '2017-08'}, [
        {'label': '2017-08-01T00:00:00', 'value': 1},
        {'label': '2017-08-06T00:00:00', 'value': 4},
        {'label': '2017-08-10T00:00:00', 'value': 1},
        {'label': '2017-08-18T00:00:00', 'value': 1},
        {'label': '2017-08-21T00:00:00', 'value': 1},
        {'label': '2017-08-22T00:00:00', 'value': 1},
        {'label': '2017-08-23T00:00:00', 'value': 1},
        {'label': '2017-08-25T00:00:00', 'value': 1},
        {'label': '2017-08-28T00:00:00', 'value': 1},
        {'label': '2017-08-29T00:00:00', 'value': 2},
        {'label': '2017-08-30T00:00:00', 'value': 1},
        {'label': '2017-08-31T00:00:00', 'value': 2}
    ]),
    # Hour
    ({'period': '2017-08-06'}, [
        {'label': '2017-08-06T01:00:00', 'value': 2},
        {'label': '2017-08-06T21:00:00', 'value': 2}
    ]),
    # Artist
    ({'filter_kind': 'artist', 'filter_value': 1, 'period': '2017-08-06'}, [
        {'label': '2017-08-06T01:00:00', 'value': 2},
        {'label': '2017-08-06T21:00:00', 'value': 2}
    ]),
    # Album
    ({'filter_kind': 'album', 'filter_value': 2}, [
        {'label': '2012-01-01T00:00:00', 'value': 1}
    ]),
    # Track
    ({'filter_kind': 'track', 'filter_value': 2}, [
        {'label': '2012-01-01T00:00:00', 'value': 1}
    ])
])
def test_count(params, data):
    assert get_count(**params) == data


@pytest.mark.parametrize('params,errors', [
    ({'extra': 'param'}, {'extra': 'Rogue field'}),
    ({'period': 'x'}, {'period': ['Invalid period: x']}),
    ({'period': '0-0-0-0-0-0'}, {'period': ['Invalid period: 0-0-0-0-0-0']}),
    ({'period': '1-1-1-1-1-1'}, {'period': ['Invalid period: 1-1-1-1-1-1']}),
    ({'period': '2012-0100-0110'}, {'period': ['Invalid period: 2012-0100-0110']}),
    ({'filter_kind': '__dict__'}, {
        'filter_kind': ["Value must be one of ['artist', 'album', 'track']."]
    }),
    ({'filter_value': 'x'}, {'filter_value': ["Value 'x' is not int."]}),
    ({'filter_kind': 'artist'}, {'filter_value': ['This field is required.']})
])
def test_invalid_params(params, errors):
    assert errors == get_count(expected_status=400, **params)['errors']
