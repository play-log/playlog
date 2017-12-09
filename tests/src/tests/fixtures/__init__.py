from functools import wraps
from pathlib import Path

from sqlalchemy import create_engine

from playlog.config import SA_URL
from playlog.models import metadata


DATA_ROOT = Path(__file__).parent / 'data'

engine = create_engine(SA_URL)


def fixture(filename):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            refresh_db()
            try:
                sql = (DATA_ROOT / '{}.sql'.format(filename)).read_text()
                with engine.begin() as conn:
                    conn.execute(sql)
                result = func(*args, **kwargs)
            finally:
                refresh_db()
            return result
        return wrapper
    return decorator


def refresh_db():
    metadata.drop_all(engine)
    metadata.create_all(engine)
