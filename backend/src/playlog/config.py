import os


def getenv(key):
    key = 'PLAYLOG_{}'.format(key)
    value = os.getenv(key)
    if value is None:
        raise ValueError('Environment variable {} is not set'.format(key))
    return value


SA_URL = getenv('SA_URL')
HOST = getenv('HOST')
PORT = int(getenv('PORT'))
