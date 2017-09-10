# Install using docker

Make sure that you have installed:

- Docker
- docker-compose
- PostgreSQL
- Redis
- NGINX

Create `docker-compose.yml`:

```yaml
version: '2'
services:
  app:
    image: playlog:%version%
    ports:
      - '5000:8000'
      - '5001:8001'
    environment:
      PLAYLOG_SA_URL: postgresql://user:password@127.0.0.1/database
      PLAYLOG_REDIS_URL: 127.0.0.1:6379
      PLAYLOG_SUBMISSIONS_BASE_URL: 'http://%your-domain%'
      PLAYLOG_SUBMISSIONS_HANDSHAKE_TIMEOUT: 30
      PLAYLOG_USER_NAME: '%your_name%'
      PLAYLOG_USER_EMAIL: '%your_email%'
      PLAYLOG_SUBMISSIONS_USER: '%your-login%'
      PLAYLOG_SUBMISSIONS_PASSWORD_HASH: '%md5_hash_of_password%'
    container_name: playlog

```

Run `docker-compose up` and `docker exec playlog ./backend/bin/alembic migrate head`

NGINX config:

```nginx
server {
    listen 80;
    server_name playlog.localhost.com;

    location / {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://127.0.0.1:5001;
    }

    location /api/ {
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_pass              http://127.0.0.1:5000/;
    }
}

```
