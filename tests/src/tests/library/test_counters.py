from tests.client import get
from tests.fixtures import fixture


def test_empty_db():
    assert get('counters') == {
        'artists': 0,
        'albums': 0,
        'tracks': 0,
        'plays': 0
    }


@fixture('counters')
def test_counters_with_data():
    assert get('counters') == {
        'artists': 1,
        'albums': 1,
        'tracks': 1,
        'plays': 1
    }
