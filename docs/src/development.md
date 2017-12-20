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
# Password: 1234
PLAYLOG_SUBMISSIONS_PASSWORD_HASH=81dc9bdb52d04dc20036dbd8313ed055

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

## Documentation

- Install [mdBook](https://github.com/rust-lang-nursery/mdBook).
- Create feature branch (`git checkout -b docs/%topic%`)
- Make your changes.
- Preview with: `bin/docs serve --open`.
- Publish changes and send a pull request.

## Contributing

- Create feature branch (`git checkout -b feature/%topic%`).
- Make changes.
- Update README.md if it's necessary.
- Commit and push (git push origin `feature/%topic%`).
- Send a pull request.
