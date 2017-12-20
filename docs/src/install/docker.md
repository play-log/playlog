# Install using docker

Make sure that you have installed:

- Docker
- docker-compose

Create `docker-compose.yml`:

```yaml
version: '3.4'
services:
  app:
    image: rossnomann/playlog:%version%
    environment:
      PLAYLOG_SA_URL: postgresql://user:password@127.0.0.1/database
      PLAYLOG_REDIS_URL: redis://127.0.0.1:6379
      PLAYLOG_SUBMISSIONS_BASE_URL: 'http://%your-domain%'
      PLAYLOG_SUBMISSIONS_HANDSHAKE_TIMEOUT: 30
      PLAYLOG_USER_NAME: '%your_name%'
      PLAYLOG_USER_EMAIL: '%your_email%'
      PLAYLOG_SUBMISSIONS_USER: '%your-login%'
      PLAYLOG_SUBMISSIONS_PASSWORD_HASH: '%md5_hash_of_password%'
    network_mode: host
    container_name: playlog

```

Don't forget to replace `%version%` and other placeholders.
Available versions are listed [here](https://hub.docker.com/r/rossnomann/playlog/tags/).

Run `docker-compose up` and `docker exec playlog ./backend/bin/alembic migrate head`

Ports:

- 8000 - API
- 8001 - Frontend

NGINX config example:

```nginx
server {
    listen 80;
    server_name %your-domain%;

    location / {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://127.0.0.1:8001;
    }

    location /api/ {
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_pass              http://127.0.0.1:8000/;
    }
}

```
