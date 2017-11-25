# Development

Requirements:

- Docker
- docker-compose
- NodeJS

Fork and clone repository:

```sh
git clone https://github.com/%username%/playlog.git
cd playlog
```

Install frontend dependencies:

```sh
cd frontend && npm install && cd ..
```

Build docker image:

```sh
./bin/build
```

Create `backend/.env` file:

```env
PLAYLOG_USER_NAME=John Doe
PLAYLOG_USER_EMAIL=johndoe@protonmail.com
PLAYLOG_SUBMISSIONS_USER=john
PLAYLOG_SUBMISSIONS_PASSWORD_HASH=81dc9bdb52d04dc20036dbd8313ed055  # 1234

```

Run app:

```sh
./bin/start
```

Run tests:

```sh
# use --build flag to rebuild image
./bin/test
```

## Contributing

- Create feature branch (git checkout -b some-feature).
- Make changes.
- Update README.md if it's necessary.
- Push (git push origin some-feature).
- Send a pull request.
