# Install manually

Ensure that you have installed:

- Python >= 3.5
- NodeJS
- PostgreSQL
- Redis
- NGINX

Clone repository:

```sh
git clone https://github.com/rossnomann/playlog.git
```

Create and activate python virtual environment:

```sh
python3 -m venv ~/.venv/playlog
source ~/.venv/playlog/bin/activate
```

Install requirements:

```sh
cd playlog/backend
pip install -r requirements/main.txt
```

Configure backend:

```sh
export PYTHONPATH=/path/to/playlog/backend/src:$PYTHONPATH
export PLAYLOG_DEBUG='false'
export PLAYLOG_SERVER_HOST='127.0.0.1'
export PLAYLOG_SERVER_PORT='8080'
export PLAYLOG_SA_URL='postgresql://playlog:password@localhost/playlog'
export PLAYLOG_REDIS_URL='127.0.0.1:6379'
export PLAYLOG_USER_NAME='John Doe'
export PLAYLOG_SUBMISSIONS_BASE_URL=http://domain/api
export PLAYLOG_SUBMISSIONS_HANDSHAKE_TIMEOUT=60
export PLAYLOG_SUBMISSIONS_USER='john'
export PLAYLOG_SUBMISSIONS_PASSWORD_HASH='md5-hash-of-password'
export PLAYLOG_USER_EMAIL='your-email-for-gravatar'
```

Run migrations:

```sh
./bin/alembic migrate head
```

Run server:

```sh
./bin/server
```

Install frontend dependencies:

```sh
cd path/to/playlog/frontend
npm install
```

Build frontend:

```sh
npm run build
```

NGINX config:

```nginx
server {
    listen      80;
    server_name domain;
    root        /path/to/playlog/frontend/build;
    error_log   /var/log/nginx/playlog.log;

    location / {
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_pass              http://127.0.0.1:8080/;
    }
}

```
