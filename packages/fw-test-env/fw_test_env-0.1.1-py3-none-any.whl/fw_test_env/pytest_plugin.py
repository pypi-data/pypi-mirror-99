"""Pytest plugin that spins up the Flywheel integration test environment."""
# pylint: disable=redefined-outer-name
import logging
import os
import re
import typing as t
from functools import partial
from pathlib import Path

import docker
import pytest
import requests
from fw_core_client import CoreClient, get_client
from fw_utils import AttrDict
from retry.api import retry_call

from . import database
from .utils import get_db, get_defaults, merge

__all__ = ["_fw", "fw", "defaults", "pytest_configure"]

DOCKER_HOST = os.getenv("DOCKER_HOST", "")
MONGO_IMG = os.getenv("FW_MONGO_IMG", "mongo:4.2")
CORE_IMG = os.getenv("FW_CORE_IMG", "flywheel/core-api:master")
STORAGE_URL = os.getenv("FW_STORAGE_URL", "osfs:///var/flywheel/data")
STORAGE_CREDS = os.getenv("FW_STORAGE_CREDS", "{}")
TEST_DATA_DIR = Path(os.environ.get("FW_TEST_DATA_DIR", "tests/data")).resolve()

AUTH_CONFIG = """
auth:
  basic:
    enabled: true
"""

CORE_CMD = f"""bash -euxc '
echo \"{AUTH_CONFIG}\" > auth.yaml;
python /src/app/bin/database.py wait_for_connection;
python /src/app/bin/database.py upgrade_schema;
gunicorn -w 1 -c /src/app/gunicorn_config.py web:app
'
"""

client_info = dict(client_name="fw-test-env", client_version="dev")

log = logging.getLogger(__name__)


def pytest_configure(config):
    """Register custom fw_data marker."""
    config.addinivalue_line("markers", "fw_data(defaults): override defaults")


@pytest.fixture(scope="session")
def _docker():
    try:
        return docker.from_env()
    except docker.errors.DockerException:  # pragma: no cover
        return pytest.skip("Docker is not available, skipping test")


@pytest.fixture(scope="session")
def _network(_docker):
    name = "fw-net"
    _docker.networks.create(name)
    yield name
    _docker.networks.get(name).remove()


@pytest.fixture(scope="session")
def _mongo(_docker, _network):
    name = "fw-core-mongo"
    _docker.containers.run(
        MONGO_IMG,
        ports={27017: 27017},
        detach=True,
        network=_network,
        name=name,
        auto_remove=True,
    )
    yield name
    _docker.containers.get(name).kill()


@pytest.fixture(scope="session")
def _core(_docker, _mongo, _network):
    name = "fw-core"
    url = f"http://{get_hostname()}:8080"
    db_url = f"mongodb://{_mongo}:27017"
    kwargs = {}
    if STORAGE_URL.startswith("osfs") and TEST_DATA_DIR.is_dir():
        # bind mount test data dir to `/var/flywheel/data/00/00`
        kwargs["volumes"] = {
            str(TEST_DATA_DIR): {"bind": "/var/flywheel/data/00/00", "mode": "rw"}
        }
    _docker.containers.run(
        CORE_IMG,
        command=CORE_CMD,
        environment={
            "SCITRAN_AUTH_CONFIG_FILE": "auth.yaml",
            "SCITRAN_PERSISTENT_DB_URI": f"{db_url}/flywheel",
            "SCITRAN_PERSISTENT_DB_LOG_URI": f"{db_url}/logs",
            "SCITRAN_PERSISTENT_FS_URL": STORAGE_URL,
            "SYSLOG_HOST": "localhost",
        },
        ports={8080: 8080},
        detach=True,
        network=_network,
        name=name,
        auto_remove=True,
        **kwargs,
    )
    retry_config = dict(
        exceptions=requests.ConnectionError, tries=15, delay=2, logger=log
    )
    retry_call(test_url, fargs=[f"{url}/api/system"], **retry_config)
    yield url
    _docker.containers.get(name).kill()


@pytest.fixture(scope="function")
def defaults(request):
    """Fixture that returns default data.

    Defaults can be overridden using the fw_data pytest marker.
    """
    marker = request.node.get_closest_marker("fw_data")
    defaults_ = get_defaults()
    if marker:
        defaults_ = merge(marker.args[0], defaults_)
    return AttrDict(**defaults_)


@pytest.fixture(scope="session")
def _fw(_core):
    """Session scoped pytest fixture that spins up the integration test environment."""
    db_url = f"mongodb://{get_hostname()}:27017/flywheel"
    file_size_fn = None
    if STORAGE_URL.startswith("osfs") and TEST_DATA_DIR.is_dir():
        file_size_fn = lambda f: Path(TEST_DATA_DIR, f).stat().st_size

    load = partial(
        database.load,
        core_url=_core,
        db_url=db_url,
        storage_url=STORAGE_URL,
        storage_creds=STORAGE_CREDS,
        file_size_fn=file_size_fn,
    )
    dump = partial(database.dump, db_url=db_url)
    reset = partial(database.reset, db_url=db_url)
    client = MagicCoreClient(_core, db_url)
    yield AttrDict(
        client=client,
        db_url=db_url,
        db=get_db(db_url),
        load=load,
        dump=dump,
        reset=reset,
        refs=database.refs,
        parents=database.parents,
    )


@pytest.fixture(scope="function")
def fw(_fw, defaults):
    """Function scoped fw pytest fixture with auto cleanup."""
    _fw.reset()
    _fw.load(defaults)
    yield _fw
    _fw.reset()


class MagicCoreClient:
    """Magic client to make easy initializing client for a given user."""

    def __init__(self, core_url: str, db_url: str):
        self.core_url = core_url
        self.db = get_db(db_url)  # pylint: disable=invalid-name

    def __getattr__(self, name: str) -> t.Any:
        api_key = self.db.apikeys.find_one({"_id": {"$regex": name}})
        if not api_key:
            raise AttributeError
        return self.get_client(api_key["_id"])

    def get_client(self, api_key: str) -> CoreClient:
        """Get client with the given api-key."""
        return get_client(api_key=api_key, url=self.core_url, **client_info)


def test_url(url):
    """Test service is available or not."""
    requests.get(url).raise_for_status()


def get_hostname():
    """Get hostname where docker services are available."""
    match = re.match(r"([^:/]+://)?(?P<host>[^:]+)(:\d+)?", DOCKER_HOST)
    return match.group("host") if match else "localhost"
