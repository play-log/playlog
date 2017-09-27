import os


def getenv(key):
    key = 'PLAYLOG_{}'.format(key.upper())
    if key not in os.environ:
        raise KeyError('Environment variable "{}" is not set'.format(key))
    value = os.environ[key]
    if not value:
        raise ValueError('Environment variable "{}" can not be empty'.format(key))
    return value


DEBUG = getenv('debug')
if DEBUG not in ['false', 'true']:
    raise ValueError(
        'Unexpected "DEBUG" value: '
        'expects "false" or "true", '
        '"{}" given'.format(DEBUG)
    )
DEBUG = DEBUG == 'true'

SERVER_HOST = getenv('server_host')
SERVER_PORT = int(getenv('server_port'))

SA_URL = getenv('sa_url')
REDIS_URL = getenv('redis_url').split(':')

USER_NAME = getenv('user_name')
USER_EMAIL = getenv('user_email')

SUBMISSIONS = {
    'base_url': getenv('submissions_base_url'),
    'handshake_timeout': int(getenv('submissions_handshake_timeout')),
    'username': getenv('submissions_user'),
    'password_hash': getenv('submissions_password_hash')
}
