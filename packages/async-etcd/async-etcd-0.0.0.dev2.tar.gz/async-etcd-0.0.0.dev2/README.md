# async-etcd
Asyncio based etcd-v3 client

## Tagging and publishing

Each push to `master` will make the CI create a development tag as `X.Y.Z.devW` and will build and push the build to pypi. Whenever a non-development version needs to be created, then do the following:
1. locally run `make bump-{patch|minor|major}`,
2. open a PR,
3. merge to `master`

The CI will detect the new untagged version and will create the corresponding tag and publish to build to pypi.
