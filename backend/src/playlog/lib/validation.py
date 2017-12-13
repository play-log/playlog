import datetime
import functools
import inspect

from schematics.models import Model
from schematics.exceptions import DataError, ValidationError as TypeValidationError
from schematics.types import BaseType


class Meta(type):
    def __getattr__(cls, attr):
        return lambda **fields: cls(attr, fields)


class validate(metaclass=Meta):
    def __init__(self, arg, fields):
        self.arg = arg
        self.schema_factory = type('Model', (Model, ), fields)

    def __call__(self, coro):
        signature = inspect.signature(coro)

        @functools.wraps(coro)
        async def wrapper(*args, **kwargs):
            bound_args = signature.bind(*args, **kwargs).arguments
            try:
                schema = self.schema_factory(bound_args.get(self.arg))
                schema.validate(convert=False)
            except DataError as exc:
                raise ValidationError(exc.to_primitive()) from exc
            bound_args[self.arg] = {k: v for k, v in schema.items() if v is not None}
            return await coro(**bound_args)

        return wrapper


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class OrderType(BaseType):
    def __init__(self, *columns):
        super().__init__(choices=columns)

    def to_native(self, value, context=None):
        if len(value) >= 2 and value[0] == '-':
            direction = 'desc'
            value = value[1:]
        else:
            direction = 'asc'
        return {
            'direction': direction,
            'column': value
        }

    def validate_choices(self, value, context):
        return super().validate_choices(value=value['column'], context=context)


class PeriodType(BaseType):
    def to_native(self, value, context=None):
        if not value:
            return

        try:
            parts = [int(x.lstrip('0')) for x in value.split('-')]
        except ValueError as exc:
            raise TypeValidationError('Invalid period: %s' % value) from exc

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
            raise TypeValidationError('Invalid period: %s' % value)

        try:
            value = datetime.datetime(*parts)
        except ValueError as exc:
            raise TypeValidationError('Invalid period: %s' % value) from exc

        return {
            'kind': kind,
            'value': value
        }
