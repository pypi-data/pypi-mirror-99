"""Functions to load, dump and reset Flywheel database."""
import datetime
import logging
import os
import random
import typing as t
from collections import defaultdict
from uuid import uuid4

from bson import ObjectId
from fw_utils import AttrDict, attrify

from .utils import get_db, get_storage

log = logging.getLogger()

BATCH_SIZE = 10000


def load(  # pylint: disable=too-many-arguments
    data: dict,
    db_url: str,
    core_url: str,
    storage_url: str,
    storage_creds: str,
    file_size_fn: t.Optional[t.Callable] = None,
) -> dict:
    """Load documents from a python dict into the core database."""
    # pylint: disable=too-many-branches
    db = get_db(db_url)
    storage = get_storage(storage_url, storage_creds)
    collection_insert_order = list(defaults).index
    refs.update(data.pop("_references", {}))

    for collection in sorted(data, key=collection_insert_order):
        batch = []
        for doc in data[collection]:
            for key, value in defaults.get(collection, {}).items():
                if key not in doc:
                    doc.setdefault(key, value() if callable(value) else value)
            if collection == "singletons" and doc["_id"] == "config":
                doc["site"].setdefault("api_url", f"{core_url}/api")
                doc["site"].setdefault("redirect_url", core_url)
            if collection == "providers" and doc["provider_class"] == "storage":
                doc.update(storage)
                storage_provider.update(doc)
            if collection == "roles":
                actions[doc["_id"]] = doc["actions"]
            if collection == "users":
                doc["email"] = doc["_id"]
            if collection == "groups":
                doc.setdefault("permissions", refs.group_perms)
            if collection in ("projects", "subjects", "sessions", "acquisitions"):
                doc.setdefault("permissions", refs.container_perms)
                last_parent_ref["id"] = doc["_id"]
                last_parent_ref["type"] = collection.rstrip("s")
            if collection == "projects":
                db.permissions_projects.insert_many(
                    dict(
                        project_id=doc["_id"],
                        user_id=perm["_id"],
                        role_id=role,
                        action=action,
                    )
                    for perm in doc["permissions"]
                    for role in perm["role_ids"]
                    for action in actions[role]
                )
            if collection == "subjects":
                doc.setdefault("code", doc["label"])
            if collection == "files":
                # TODO make passing test files more intuitive (not only by uuid)
                if file_size_fn:
                    doc.setdefault("size", file_size_fn(doc["uuid"]))
                doc.setdefault("name", os.path.basename(doc["uuid"]))
                doc.setdefault("provider_id", storage_provider["_id"])
                doc.setdefault("parent_ref", file_parent_ref())
                doc.setdefault("parents", file_parents(doc["parent_ref"]))
            # track parents
            if "parents" in doc:
                if collection == "files":
                    key = doc["_id"]["file_id"]
                else:
                    key = doc["_id"]
                parents[key] = doc["parents"]
            ids[collection].append(doc["_id"])
            batch.append(doc)
            if len(batch) >= BATCH_SIZE:
                db[collection].insert_many(batch)
                batch = []
        if batch:
            db[collection].insert_many(batch)
    log.info("Finished inserting data")
    return data


def dump(db_url: str) -> AttrDict:
    """Dump core database documents and return as a python dict."""
    db = get_db(db_url)
    collections = db.list_collection_names()
    return attrify({coll: list(db[coll].find({})) for coll in collections})


def reset(db_url: str) -> None:
    """Reset database state, remove all loaded data."""
    db = get_db(db_url)
    for collection in db.list_collection_names():
        db[collection].delete_many({})
    actions.clear()
    refs.clear()
    ids.clear()
    parents.clear()
    last_parent_ref.clear()


def file_parents(parent_ref):
    """Return parents dictionary based on a file parent ref."""
    parents_ = {parent_ref["type"]: parent_ref["id"]}
    parents_.update(parents.get(parent_ref["id"], {}))
    return parents_


def file_parent_ref():
    """Get last container as parent ref for file."""
    if not last_parent_ref:
        raise ValueError("Can't determine parent for file")
    return last_parent_ref


def required(field: str) -> None:
    """Raise ValueError about a missing required field."""
    raise ValueError(f"{field} is required")


oid = ObjectId
now = lambda: datetime.datetime.utcnow().replace(microsecond=0)
age = lambda: random.randint(20, 80)
sex = lambda: random.choice(["male", "female", "unknown"])
uuid = lambda: str(uuid4())

# common document fields - helpers for building default_fields
timestamp_fields = dict(created=now, modified=now)
revision_fields = dict(revision=1, **timestamp_fields)
container_fields = dict(notes=[], tags=[], info={}, **revision_fields)

# collection to list of document _ids - {coll: list[_id]}
# global tracking enables
# - generated labels using self.count (eg. acquisition-42)
# - automatic referencing of parent containers via self.last
ids: t.Dict[str, list] = defaultdict(list)
parents: t.Dict[ObjectId, t.Dict[str, ObjectId]] = defaultdict(dict)
refs = AttrDict()
last_parent_ref = AttrDict()
storage_provider: dict = {}
# role _id to list of role actions - {_id: list[action]}
actions: t.Dict[str, t.List[str]] = {}
count = lambda collection: len(ids[collection])
last = lambda collection: str(ids[f"{collection}s"][-1])
last_oid = lambda collection: ids[f"{collection}s"][-1]


defaults: dict = dict(
    singletons=dict(
        _id=lambda: required("singleton._id"),
    ),
    providers=dict(
        _id=oid,
        provider_class="storage",  # compute|storage
        provider_type="local",  # compute:static|... storage:local|aws|gc
        config={},
        origin=dict(type="system", id="system"),
        **timestamp_fields,
    ),
    roles=dict(_id=oid, label=lambda: f"role-{count('roles')}"),
    modalities=dict(active=True, classification={}),
    devices=dict(
        _id=oid,
        label=lambda: f"device-{count('devices')}",
        name="device",
        type="device",
        errors=[],
        last_seen=now,
        disabled=False,
    ),
    users=dict(
        _id=lambda: f"user-{count('users')}@flywheel.test",
        user_id=oid,
        firstname=lambda: f"UserFirstname{count('users')}",
        lastname=lambda: f"UserLastname{count('users')}",
        firstlogin=now,
        lastlogin=now,
        roles=["user"],
        avatars={},
        **revision_fields,
    ),
    apikeys=dict(
        _id=lambda: required("apikey._id"),
        type="user",  # device|user|job
        origin=lambda: required("apikey.origin"),
        scope=None,
        created=now,
        last_used=now,
    ),
    groups=dict(
        _id=lambda: f"group-{count('groups')}",
        label=lambda: f"group-{count('groups')}",
        editions={"lab": False},
        providers={},
        roles=[],
        permissions_template=[],
        tags=[],
        **revision_fields,
    ),
    projects=dict(
        _id=oid,
        label=lambda: f"project-{count('projects')}",
        parents=lambda: dict(group=last("group")),
        group=lambda: last("group"),
        editions={"lab": False},
        providers={},
        templates=[],
        **container_fields,
    ),
    subjects=dict(
        _id=oid,
        label=lambda: f"subject-{count('subjects')}",
        parents=lambda: dict(group=last("group"), project=last_oid("project")),
        project=lambda: last_oid("project"),
        firstname=lambda: f"SubjectFirstname{count('subjects')}",
        lastname=lambda: f"SubjectLastname{count('subjects')}",
        age=age,
        sex=sex,
        **container_fields,
    ),
    sessions=dict(
        _id=oid,
        uid=lambda: f"session-{count('sessions')}",
        label=lambda: f"session-{count('sessions')}",
        parents=lambda: dict(
            group=last("group"),
            project=last_oid("project"),
            subject=last_oid("subject"),
        ),
        subject=lambda: last_oid("subject"),
        timestamp=lambda: now().isoformat(),
        timezone="UTC",
        **container_fields,
    ),
    acquisitions=dict(
        _id=oid,
        uid=lambda: f"acquisition-{count('acquisitions')}",
        label=lambda: f"acquisition-{count('acquisitions')}",
        parents=lambda: dict(
            group=last("group"),
            project=last_oid("project"),
            subject=last_oid("subject"),
            session=last_oid("session"),
        ),
        session=lambda: last_oid("session"),
        timestamp=lambda: now().isoformat(),
        timezone="UTC",
        **container_fields,
    ),
    files=dict(
        _id=lambda: dict(file_id=oid(), revision=1),
        uuid=lambda: required("file.uuid"),
        type=None,
        mimetype="application/text",
        modality=None,
        classification={},
        tags=[],
        info={},
        origin=dict(type="system", id="system"),
        **timestamp_fields,
    ),
)
