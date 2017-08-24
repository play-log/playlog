from datetime import datetime

from schema import SchemaError


class Int(object):
    def __init__(self, *, min_val=None, max_val=None):
        self.__min_val = min_val
        self.__max_val = max_val

    def validate(self, data):
        try:
            data = int(data)
        except ValueError:
            raise SchemaError('%s is not an integer' % data)
        if self.__min_val is not None and data < self.__min_val:
            raise SchemaError('%d must be greater than %d' % (data, self.__min_val))
        if self.__max_val is not None and data > self.__max_val:
            raise SchemaError('%d must be less than %d' % (data, self.__max_val))
        return data


class Length(object):
    def __init__(self, *, min_len, max_len):
        self.__min_len = min_len
        self.__max_len = max_len

    def validate(self, data):
        length = len(data)
        if self.__min_len > length:
            raise SchemaError('Lenght must be greater than %d' % self.__min_len)
        if self.__max_len < length:
            raise SchemaError('Length must be less than %d' % self.__max_len)
        return data


class DateTime(object):
    def __init__(self, fmt):
        self.__fmt = fmt

    def validate(self, data):
        try:
            return datetime.strptime(data, self.__fmt)
        except Exception as e:
            raise SchemaError('%s is not a valid date' % data)


class ISODate(DateTime):
    def __init__(self):
        super().__init__('%Y-%m-%d')


class OneOf(object):
    def __init__(self, choices):
        self.__choices = choices

    def validate(self, data):
        if data not in self.__choices:
            raise SchemaError('%s is not one of %s' % (data, self.__choices))
        return data
