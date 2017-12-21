# How to release a new version

1. Ensure development requirements.
1. Run tests.
1. Update documentation, README and other stuff (if required).
1. Update CHANGELOG (`docs/src/changelog.md`).
1. Update TODO (`docs/src/todo.md`)
1. Run `bin/build production <version>`, where `<version>` is a target version.
1. Push the image to docker hub `docker push rossnomann/playlog:<version>`.
1. Make a release on GitHub.
