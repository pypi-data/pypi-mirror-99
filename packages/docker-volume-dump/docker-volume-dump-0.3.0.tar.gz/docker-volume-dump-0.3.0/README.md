[![pipeline status](https://gitlab.com/micro-entreprise/docker-volume-dump/badges/master/pipeline.svg)](https://gitlab.com/micro-entreprise/docker-volume-dump/commits/master)

[![coverage report](https://gitlab.com/micro-entreprise/docker-volume-dump/badges/master/coverage.svg)](https://gitlab.com/micro-entreprise/docker-volume-dump/commits/master)

# Docker volume dump

A tool to help archive data from container running in a docker container.

At the moment postgresql and mysql/mariadb dumps are supported.

## Usage

### Using docker

```bash
docker run registry.gitlab.com/micro-entreprise/docker-volume-dump archive --help
```

For instance if you want to create dumps from different postgresql container
in a docker swarm environment this would looks likes:

```
docker service create \
          -d \
          --mode global \
          --name pgsql-dumps \
          --restart-condition none \
          --mount type=bind,src=/path-to-dump-storage/,dst=/backups \
          --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
          --mount type=bind,src=/path-to-config-directory/,dst=/etc/archiver \
          --network sentry_internal \
          --with-registry-auth registry.gitlab.com/micro-entreprise/docker-volume-dump \
          archive -f /etc/archiver/logging.json -r -s '{"label": ["docker-volume-dump.project='$PROJECT'","docker-volume-dump.environment='$ENVIRONMENT'"]}'
```

This script require access to the docker daemon to query docker labels.
It must be launched on each host using `--mode global`.

### Using python

```bash
pip install docker-volume-dump
archive --help
```

## Configuration

The main idea is to tell the container how to manage its backups using docker
labels, you can set following labels

- **docker-volume-dump.driver**: Optional (`pgsql` by default) kind of data to
  restore (could be one of `pgsql`, `mysql`)

  > **Note**: `mysql` driver is working for mariadb as well

- **docker-volume-dump.isactive**: Takes no value. Determine if the Archiver backups are enabled on the container. Default selector to get containers to handle.
- **docker-volume-dump.driver**: The Archiver driver to use (pgsql, mysql). Only one value supported by container
- **docker-volume-dump.dbname**: Required if database driver, the database to save
- **docker-volume-dump.username**: DB role used to dump the db
- **docker-volume-dump.password**: DB password used to dump the db. Required if driver is mysql
- **docker-volume-dump.project**: A project name (the container name if not set)
- **docker-volume-dump.environment**: An environment (staging, production, ...)
- **docker-volume-dump.prefix**: A prefix for the dump file

This will generate a file in a tree likes

`<project>/[<environment>/]<prefix><dbname><date>`

## Realase process

```bash
pip install -U pip wheel bump2version twine
python setup.py sdist bdist_wheel
twine check dist/*
twine upload
```

## Roadmap

- [ ] setup pre-commit with common lint tools
- [ ] automaticaly publish on pypi
- [ ] Handle volume data files
- [ ] wondering if the way use to query docker labels is compliant with k8s
- [ ] In swarm investigate to launch only once container (not on each hosts)
