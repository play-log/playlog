import os


def getenv(key):
    key = 'PLAYLOG_{}'.format(key)
    value = os.getenv(key)
    if value is None:
        raise ValueError('Environment variable {} is not set'.format(key))
    return value


ENVIRONMENT = getenv('ENVIRONMENT')

HOST = getenv('HOST')
PORT = int(getenv('PORT'))

SA_URL = getenv('SA_URL')

USER_NAME = getenv('USER_NAME')
USER_EMAIL = getenv('USER_EMAIL')
