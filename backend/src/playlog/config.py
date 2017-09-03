import os


def getenv(key):
    key = 'PLAYLOG_{}'.format(key)
    value = os.getenv(key)
    if value is None:
        raise ValueError('Environment variable {} is not set'.format(key))
    return value


ENVIRONMENT = getenv('ENVIRONMENT')

SERVER_HOST = getenv('SERVER_HOST')
SERVER_PORT = int(getenv('SERVER_PORT'))

SA_URL = getenv('SA_URL')
REDIS_URL = getenv('REDIS_URL').split(':')

USER_NAME = getenv('USER_NAME')
USER_EMAIL = getenv('USER_EMAIL')

SUBMISSIONS = {
    'username': getenv('SUBMISSIONS_USER'),
    'password_hash': getenv('SUBMISSIONS_PASSWORD_HASH')
}
