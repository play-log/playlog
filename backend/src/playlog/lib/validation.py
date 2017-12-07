import datetime
import functools
import inspect

import schema


def validate(**definition):
    keys = list(definition.keys())
    definition = _swap_optional(definition)
    s = schema.Schema(definition)

    def decorator(coro):
        signature = inspect.signature(coro)

        @functools.wraps(coro)
        async def wrapper(*args, **kwargs):
            bound_args = signature.bind_partial(*args, **kwargs).arguments
            raw = dict(filter(lambda t: t[0] in keys, bound_args.items()))
            try:
                validated = s.validate(raw)
            except schema.SchemaError as exc:
                raise ValidationError([i for i in exc.autos if i is not None]) from exc
            bound_args.update(validated)
            return await coro(**bound_args)

        return wrapper

    return decorator


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class Optional(object):
    def __init__(self, value):
        self.value = value


def _swap_optional(data):
    result = {}
    for k, v in data.items():
        if isinstance(v, Optional):
            k = schema.Optional(k)
            v = v.value
        if isinstance(v, dict):
            v = _swap_optional(v)
        result[k] = v
    return result


class Int(object):
    def __init__(self, *, min_val=None, max_val=None):
        self.__min_val = min_val
        self.__max_val = max_val

    def validate(self, data):
        try:
            data = int(data)
        except ValueError:
            raise schema.SchemaError('%s is not an integer' % data)
        if self.__min_val is not None and data < self.__min_val:
            raise schema.SchemaError('%d is less than %d' % (data, self.__min_val))
        if self.__max_val is not None and data > self.__max_val:
            raise schema.SchemaError('%d is greater than %d' % (data, self.__max_val))
        return data


class Length(object):
    def __init__(self, *, min_len, max_len):
        self.__min_len = min_len
        self.__max_len = max_len

    def validate(self, data):
        length = len(data)
        if self.__min_len > length:
            raise schema.SchemaError('Length must be greater than %d' % self.__min_len)
        if self.__max_len < length:
            raise schema.SchemaError('Length must be less than %d' % self.__max_len)
        return data


class DateTime(object):
    def __init__(self, fmt):
        self.__fmt = fmt

    def validate(self, data):
        try:
            return datetime.datetime.strptime(data, self.__fmt)
        except Exception as e:
            raise schema.SchemaError('%s is not a valid date' % data)


class ISODate(DateTime):
    def __init__(self):
        super().__init__('%Y-%m-%d')


class ISODateTime(DateTime):
    def __init__(self):
        super().__init__('%Y-%m-%dT%H:%M')


class OneOf(object):
    def __init__(self, choices):
        self.__choices = choices

    def validate(self, data):
        if data not in self.__choices:
            raise schema.SchemaError('%s is not one of %s' % (data, self.__choices))
        return data


class Period(object):
    def validate(self, data):
        if not data:
            return

        try:
            parts = [int(x.lstrip('0')) for x in data.split('-')]
        except ValueError as exc:
            raise schema.SchemaError('Invalid period: %s' % data) from exc

        parts_len = len(parts)
        if parts_len == 1:
            kind = 'year'
            parts += [1, 1]
        elif parts_len == 2:
            kind = 'month'
            parts.append(1)
        elif parts_len == 3:
            kind = 'day'
        else:
            raise schema.SchemaError('Invalid period: %s' % data)

        try:
            value = datetime.datetime(*parts)
        except ValueError:
            raise schema.SchemaError('Invalid period: %s' % data)

        return {
            'kind': kind,
            'value': value
        }
