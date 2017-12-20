# Configuration

## Server

Server reads config from the following environment variables:

- `PLAYLOG_DEBUG` - Debug mode: `true` or `false`.
- `PLAYLOG_SERVER_HOST` - TCP/IP hostname to serve on.
- `PLAYLOG_SERVER_PORT` - TCP/IP port to serve on.
- `PLAYLOG_SA_URL` - SQLAlchemy URL in the following format: `postgresql://user:pass@host:port/database`.
- `PLAYLOG_REDIS_URL` - Redis URL like `redis://127.0.0.1:6379/0`.
- `PLAYLOG_USER_NAME` - An arbitrary username (John Doe for example).
- `PLAYLOG_USER_EMAIL` - Your email (currently used for gravatar only, not required).
- `PLAYLOG_SESSION_LIFETIME` - User session lifetime in seconds.
- `PLAYLOG_SUBMISSIONS_BASE_URL` - Base URL for submissions handshake response
  (`http://127.0.0.1:5051` for example).
- `PLAYLOG_SUBMISSIONS_HANDSHAKE_TIMEOUT` - Submissions handshake timeout in seconds (30 should be enough).
- `PLAYLOG_SUBMISSIONS_USER` - Login for submissions API.
- `PLAYLOG_SUBMISSIONS_PASSWORD_HASH` - MD5 hash of password for submissions API.

## Client

Make sure that your player supports [Last.fm Submissions Protocol](https://www.last.fm/api/submissions).

- Scrobbling address: <http://your-host/api/submissions>
- Username: a value from `PLAYLOG_SUBMISSIONS_USER`
- Password: a string used for `PLAYLOG_SUBMISSIONS_PASSWORD_HASH`

Note: If you are not able to specify scrobbling address,
you can try to setup a proxy (using NGINX for example).
