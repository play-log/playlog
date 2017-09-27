import os


def getenv(key):
    key = 'PLAYLOG_{}'.format(key)
    value = os.getenv(key)
    if value is None:
        raise ValueError('Environment variable {} is not set'.format(key))
    return value


DEBUG = getenv('DEBUG')
if DEBUG not in ['false', 'true']:
    raise ValueError(
        'Unexpected "DEBUG" value: '
        'expects "false" or "true", '
        '"{}" given'.format(DEBUG)
    )
DEBUG = DEBUG == 'true'

SERVER_HOST = getenv('SERVER_HOST')
SERVER_PORT = int(getenv('SERVER_PORT'))

SA_URL = getenv('SA_URL')
REDIS_URL = getenv('REDIS_URL').split(':')

USER_NAME = getenv('USER_NAME')
USER_EMAIL = getenv('USER_EMAIL')

SUBMISSIONS = {
    'base_url': getenv('SUBMISSIONS_BASE_URL'),
    'handshake_timeout': int(getenv('SUBMISSIONS_HANDSHAKE_TIMEOUT')),
    'username': getenv('SUBMISSIONS_USER'),
    'password_hash': getenv('SUBMISSIONS_PASSWORD_HASH')
}
