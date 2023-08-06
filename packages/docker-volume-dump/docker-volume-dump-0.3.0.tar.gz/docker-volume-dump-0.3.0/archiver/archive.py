import argparse
import docker
import json
import logging.config
import os
import tarfile

from datetime import datetime
from pathlib import Path

from abc import ABCMeta

DTFORMAT = "%Y-%m-%dT%H%M%S.%f"
DEFAULT_ROOT_DIRECTOY = '/backups'
DEFAULT_CT_DIRECTORY = '/tmp'
DEFAULT_SELECTOR = '{"label": "docker-volume-dump.isactive"}'

logger = logging.getLogger(__name__)


def backup():
    parser = argparse.ArgumentParser(
        description="Backup all targeted containers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    backup_group = parser.add_argument_group(
        'Backup options'
    )
    backup_group.add_argument(
        '-d',
        '--backup-directory',
        default=DEFAULT_ROOT_DIRECTOY,
        help="Where backups will be stored"
    )
    backup_group.add_argument(
        '-s',
        '--selector',
        default=DEFAULT_SELECTOR,
        type=json.loads,
        help="A json string to select container to backup. "
             "Likes docker ps --filter option"
    )
    backup_group.add_argument(
        '-r',
        '--raise-on-failure',
        action='store_true'
    )
    logging_group = parser.add_argument_group(
        'Logging params'
    )
    logging_group.add_argument(
        '-f',
        '--logging-file',
        type=argparse.FileType('r'),
        help='Logging configuration file, (logging-level and logging-format '
             'are ignored if provide)'
    )
    logging_group.add_argument(
        '-l', '--logging-level', default='INFO'
    )
    logging_group.add_argument(
        '--logging-format',
        default='%(asctime)s - %(levelname)s (%(module)s%(funcName)s): '
                '%(message)s'
    )
    arguments = parser.parse_args()
    logging.basicConfig(
        level=getattr(logging, arguments.logging_level.upper()),
        format=arguments.logging_format
    )
    if arguments.logging_file:
        try:
            json_config = json.loads(arguments.logging_file.read())
            logging.config.dictConfig(json_config)
        except json.JSONDecodeError:
            logging.config.fileConfig(arguments.logging_file.name)

    Archiver(selector=arguments.selector,
             root_directory=arguments.backup_directory,
             raise_on_failure=arguments.raise_on_failure
             ).backup_all()


class DriverFactory(metaclass=ABCMeta):

    @staticmethod
    def get_driver(drivername, container_directory,
                   root_directory, raise_on_failure):
        default_env_vars_dict = {"env_vars_prefix": "POSTGRES_",
                                 "db_name": "POSTGRES_DB",
                                 "db_username": "POSTGRES_USER",
                                 "db_password": "POSTGRES_PASSWORD"}

        if drivername == 'mysql':
            return MysqlDriver(
                container_directory=container_directory,
                root_directory=root_directory,
                raise_on_failure=raise_on_failure,
                env_vars_dict={"env_vars_prefix": "MYSQL_",
                               "db_name": "MYSQL_DATABASE",
                               "db_username": "MYSQL_USER",
                               "db_password": "MYSQL_PASSWORD"}
            )
        elif drivername == 'pgsql':
            return PgsqlDriver(
                container_directory=container_directory,
                root_directory=root_directory,
                raise_on_failure=raise_on_failure,
                env_vars_dict={"env_vars_prefix": "POSTGRES_",
                               "db_name": "POSTGRES_DB",
                               "db_username": "POSTGRES_USER",
                               "db_password": "POSTGRES_PASSWORD"}
            )
        return PgsqlDriver(
            container_directory=container_directory,
            root_directory=root_directory,
            raise_on_failure=raise_on_failure,
            env_vars_dict=default_env_vars_dict
        )


class Archiver():
    """Archiver class aims to find containers, create backups
    and move that backups to the expected directory.

    by default select all containers
    """

    def __init__(
            self,
            selector=None,
            root_directory=DEFAULT_ROOT_DIRECTOY,
            container_directory=DEFAULT_CT_DIRECTORY,
            docker_cli=None,
            raise_on_failure=True
    ):
        """Instantiate

        :param selector:
            a dict used to select containers, it's exactly the same
            as `list() filters params from docker python lib
            <https://docker-py.readthedocs.io/en/stable/
            containers.html#docker.models.containers.ContainerCollection.list
            >`_
        :param root_directory: the root directory where dumps are saved.
        :param container_directory: the root directory where dumps is done
            inside the postgres container.
        :param docker_cli: An instance of `docker.DockerClient <https://
            docker-py.readthedocs.io/en/stable/client.html>`_. Create a new
            one if none
        """
        if not selector:
            selector = dict(label="docker-volume-dump.isactive")
        if not docker_cli:
            docker_cli = docker.DockerClient()
        self._docker = docker_cli
        self._selector = selector
        self._root_directory = root_directory
        self._container_directory = container_directory
        self._raise = raise_on_failure

    def backup_all(self):
        """Backup all targeted containers

        :return: list of created filename
        """

        dumps = []
        containers = self._docker.containers.list(filters=self._selector)
        logger.info(
            "Found %i containers using following selector: %r.",
            len(containers),
            self._selector
        )
        for container in containers:
            driver = DriverFactory.get_driver(
                container.labels.get('docker-volume-dump.driver'),
                self._container_directory,
                self._root_directory,
                self._raise)
            dbenvs = {
                env.split("=")[0]: env.split("=")[1] for env in
                container.attrs.get("Config", {}).get("Env", [])
                if env.startswith(driver._env_vars_dict["env_vars_prefix"])
            }
            dbname = container.labels.get('docker-volume-dump.dbname')
            if not dbname:
                dbname = dbenvs.get(driver._env_vars_dict["db_name"])
            if not dbname:
                logger.warning(
                    "Ignoring '%s' docker container because we couldn't "
                    "find dbname to dump while processing "
                    "backup using selector: %r", container.name, self._selector
                )
                continue
            username = container.labels.get('docker-volume-dump.username')
            if not username:
                username = dbenvs.get(driver._env_vars_dict["db_username"])
            if not username:
                logger.warning(
                    "Ignoring '%s' docker container because we couldn't "
                    "find username to dump while processing "
                    "backup using selector: %r", container.name, self._selector
                )
                continue
            password = container.labels.get('docker-volume-dump.password')
            if not password:
                password = dbenvs.get(driver._env_vars_dict["db_password"])
            if not password:
                logger.warning(
                    "Processing '%s' docker container "
                    "backup without db password"
                    "because we couldn't find password value while processing "
                    "backup using selector: %r", container.name, self._selector
                )
            project = container.labels.get('docker-volume-dump.project')
            environment = container.labels.get(
                'docker-volume-dump.environment'
            )
            prefix = container.labels.get('docker-volume-dump.prefix')
            try:
                dump_path = driver.backup(
                    container,
                    dbname,
                    username,
                    password,
                    project,
                    environment,
                    prefix
                )
            except docker.errors.DockerException as err:
                logger.error(
                    "Docker Exception: The following dump fails, "
                    "please figure out what's "
                    "happens: dump: %s - container: %r - error: %r",
                    dbname, container, err
                )
                if self._raise:
                    raise err
                continue
            except Exception as err:
                logger.error(
                    "The following dump fails, please figure out what's "
                    "happen: conainer name: %s - dbname: %s - "
                    "container labels: %r - error: %r",
                    container.name, dbname, container.labels, err
                )
                if self._raise:
                    raise err
                continue

            if dump_path:
                logger.info(
                    "[%s-%s] Saving db: %s from %s into %s",
                    project, environment, dbname, container.name, dump_path
                )
                # Todo: monitor success dump
                # https://github.com/prometheus/client_python#exporting-to-a-pushgateway
                dumps.append(dump_path)
        return dumps

    def backup(
        self, container, dbname, username=None, password=None, project=None,
        environment=None, prefix=None
    ):
        """backup a database

        :param container: the Database container host
        :param dbname: the Database name
        :param username String (Optional): user name
        :param password String (Optional): password
        :param project String (Optional): project name
        :param environment String (Optional): environment
        :param prefix String (Optional): a prefix to add to the name
        :return: backup path

        ``project``, ``environment`` and ``prefix`` are used to build the
        backup filename ``<project>/[<environment>/]<prefix><dbname><date>``
        """

        logger.info(
            "[%s-%s]dumping %s from %s ct",
            project, environment, dbname, container.name
        )
        if not project:
            project = container.name
        if not username:
            username = 'postgres'
        if not password:
            password = 'postgres'
        if not environment:
            environment = ''
        if not prefix:
            prefix = ''
        filename = "{}{}-{}.sql.gz".format(
            prefix,
            dbname,
            datetime.now().strftime(DTFORMAT)
        )
        container_path = os.path.join(
            self._container_directory,
            project,
            environment,
            filename
        )
        host_dump_path = os.path.join(
            self._root_directory,
            project,
            environment,
            filename
        )
        host_tar_path = host_dump_path + '.tar'
        self.execute_cmd_in_container(
            container,
            self.get_dump_command(container_path, username, dbname, password),
            project
        )
        Path(os.path.dirname(host_tar_path)).mkdir(parents=True, exist_ok=True)
        stream, stat = container.get_archive(container_path)
        with open(host_tar_path, 'wb') as dump:
            for buffer in stream:
                dump.write(buffer)
        self.untar(host_tar_path)
        if os.path.isfile(host_dump_path):
            self.execute_cmd_in_container(
                container,
                'rm -r {}'.format(
                    os.path.join(self._container_directory, project)
                ),
                project
            )
            return host_dump_path
        return

    def untar(self, path):
        tar = tarfile.open(path)
        tar.extractall(path=os.path.dirname(path))
        tar.close()
        os.remove(path)

    def execute_cmd_in_container(self, container, command, project):
        res = container.exec_run(
            "sh -c '{}'".format(command)
        )
        if res.exit_code:
            raise RuntimeError(
                "The following error happens "
                "(while running: {}) on project {}: {}".format(
                    command,
                    project,
                    res.output
                )
            )
        return res

    def get_dump_command(self, container_path, username, dbname,
                         password=None):
        pass


class PgsqlDriver(Archiver):
    """Archiver subclass for PostgreSQL dumps
    """

    def __init__(self, container_directory=DEFAULT_CT_DIRECTORY,
                 root_directory=DEFAULT_ROOT_DIRECTOY,
                 raise_on_failure=True,
                 env_vars_dict={}):
        self._container_directory = container_directory
        self._root_directory = root_directory
        self._raise = raise_on_failure
        self._env_vars_dict = env_vars_dict

    def get_dump_command(self, container_path, username,
                         dbname, password=None):
        command = 'mkdir -p {}; pg_dump -U {} -Fc -O -f "{}" {}'.format(
                  os.path.dirname(container_path),
                  username,
                  container_path,
                  dbname)
        return command


class MysqlDriver(Archiver):
    """Archiver subclass for MySQL dumps
    """

    def __init__(self, container_directory=DEFAULT_CT_DIRECTORY,
                 root_directory=DEFAULT_ROOT_DIRECTOY,
                 raise_on_failure=True,
                 env_vars_dict={}):
        self._container_directory = container_directory
        self._root_directory = root_directory
        self._raise = raise_on_failure
        self._env_vars_dict = env_vars_dict

    def get_dump_command(self, container_path, username, dbname, password):
        command = 'mkdir -p {}; mysqldump -u {} -p{} {} | gzip > {}'.format(
                  os.path.dirname(container_path),
                  username,
                  password,
                  dbname,
                  container_path)
        return command
