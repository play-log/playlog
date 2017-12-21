# Upgrading from previous versions

1. Read [changelog](changelog.html).
1. Stop application.
1. Create a backup.
1. Checkout to a new version or pull a new [docker image](https://hub.docker.com/r/rossnomann/playlog/tags/).
1. Update configuration parameters (if required, there should be a note in changelog).
1. Update dependencies in case of manual installation (see [install section](install/manual.html)).
1. Run migrations:
   - `docker exec playlog ./backend/bin/alembic migrate head`
   - or just `bin/alembic migrate head` if you've installed manually.
1. Launch application.
