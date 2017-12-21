# Changelog

## 0.2.0 (21.12.2017)

### New features

- Interactive date charts.

### Bug fixes

- `last_play` date now is correct.
- Return 404 when artist, album or track not found (currently on backend only).

### Breaking changes

- `PLAYLOG_ENVIRONMENT` environment variable was removed in favor of `PLAYLOG_DEBUG`.
- `PLAYLOG_REDIS_URL` now requires `redis://` prefix.

### Other notable changes

- Added support for `docker-compose.overrides.yml` in development environment.
- `docker-compose` files updated to v3.4.
- `PLAYLOG_USER_EMAIL` environment variable is no longer required.
- Added tests.

## 0.1.0 (10.09.2017)

- First Release.
