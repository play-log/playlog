import json

from datetime import datetime
from functools import partial

from aiopg.sa.result import RowProxy


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, RowProxy):
            result = {key: o[key] for key in o.keys()}
        elif isinstance(o, datetime):
            result = o.isoformat()
        else:
            result = super().default(o)
        return result


dumps = partial(json.dumps, cls=Encoder)
