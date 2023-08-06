"""Utility classes/methods."""
import functools
import json
from pathlib import Path

import bson
import pymongo
import yaml


def merge(data: dict, defaults: dict) -> dict:  # pylint: disable=redefined-outer-name
    """Return data merged with defaults."""
    for key, value in defaults.items():
        data.setdefault(key, value)
    return data


def get_storage(storage_url: str, storage_creds: str) -> dict:
    """Return storage provider configuration from url/creds or envvars."""
    if storage_url.startswith("osfs://"):
        storage_type = "local"
    if storage_url.startswith("s3://"):
        storage_type = "aws"  # pragma: no cover
    if storage_url.startswith("gc://"):
        storage_type = "gc"  # pragma: no cover
    return dict(
        provider_type=storage_type,
        config=dict(path=storage_url),
        creds=json.loads(storage_creds),
    )


@functools.lru_cache()
def get_db(db_uri: str) -> pymongo.MongoClient:
    """Return pymongo db client."""
    return pymongo.MongoClient(
        db_uri, serverSelectionTimeoutMS=2 * 60 * 1000
    ).get_default_database()


@functools.lru_cache()
def get_defaults() -> dict:
    """Return the built-in defaults loaded from the co-located YAML file."""
    return yaml.safe_load(open(Path(__file__).parent / "defaults.yml"))


# additional yaml constructors and representers


def split_constructor(loader, data):
    """Load a single string separated by whitespace as a list of strings."""
    return loader.construct_scalar(data).split()


def objectid_constructor(loader, data):
    """Load a 24-char hex string into a bson.ObjectId."""
    return bson.ObjectId(loader.construct_scalar(data) or None)


yaml.SafeLoader.add_constructor("!split", split_constructor)
yaml.SafeLoader.add_constructor("!ObjectId", objectid_constructor)
