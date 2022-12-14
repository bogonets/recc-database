# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional

from recc_database.chrono.datetime import tznow
from recc_database.database.query_builder import BuildResult, UpdateBuilder
from recc_database.variables.database import (
    ROLE_SLUG_DEVELOPER,
    ROLE_SLUG_GUEST,
    ROLE_SLUG_MAINTAINER,
    ROLE_SLUG_OWNER,
    ROLE_SLUG_REPORTER,
    TABLE_GROUP_MEMBER,
    TABLE_PROJECT_MEMBER,
    TABLE_ROLE,
)

INSERT_ROLE = f"""
INSERT INTO {TABLE_ROLE} (
    slug,
    name,
    description,
    extra,
    hidden,
    lock,
    created_at,
    updated_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $7
) RETURNING uid;
"""

DELETE_ROLE_BY_UID = f"""
DELETE FROM {TABLE_ROLE}
WHERE uid=$1;
"""

SELECT_ROLE_UID_BY_SLUG = f"""
SELECT uid
FROM {TABLE_ROLE}
WHERE slug=$1;
"""

SELECT_ROLE_SLUG_BY_UID = f"""
SELECT slug
FROM {TABLE_ROLE}
WHERE uid=$1;
"""

SELECT_ROLE_BY_UID = f"""
SELECT *
FROM {TABLE_ROLE}
WHERE uid=$1;
"""

SELECT_ROLE_LOCK_BY_UID = f"""
SELECT lock
FROM {TABLE_ROLE}
WHERE uid=$1;
"""

SELECT_ROLE_ALL = f"""
SELECT *
FROM {TABLE_ROLE};
"""

EXISTS_ROLE_BY_UID = f"""
SELECT EXISTS(
    SELECT *
    FROM {TABLE_ROLE}
    WHERE uid=$1
);
"""

SELECT_ROLE_BY_USER_UID_AND_GROUP_UID = f"""
WITH gm AS (
    SELECT role_uid
    FROM {TABLE_GROUP_MEMBER}
    WHERE user_uid=$1 AND group_uid=$2
)
SELECT perm.*
FROM {TABLE_ROLE} AS perm, gm
WHERE gm.role_uid=perm.uid;
"""

SELECT_ROLE_BY_USER_UID_AND_PROJECT_UID = f"""
WITH pm AS (
    SELECT role_uid
    FROM {TABLE_PROJECT_MEMBER}
    WHERE user_uid=$1 AND project_uid=$2
)
SELECT perm.*
FROM {TABLE_ROLE} AS perm, pm
WHERE pm.role_uid=perm.uid;
"""

_INSERT_ROLE_SIMPLY_FORMAT = f"""
INSERT INTO {TABLE_ROLE} (
    slug,
    name,
    hidden,
    lock,
    created_at,
    updated_at
) VALUES (
    '{{slug}}',
    '{{name}}',
    {{hidden}},
    {{lock}},
    '{{created_at}}',
    '{{created_at}}'
);
"""


def _insert_role_simply(
    slug: str,
    name: Optional[str] = None,
    hidden=False,
    lock=False,
    created_at: Optional[datetime] = None,
) -> str:
    created = created_at if created_at else tznow()
    return _INSERT_ROLE_SIMPLY_FORMAT.format(
        slug=slug,
        name=name if name else slug,
        hidden=hidden,
        lock=lock,
        created_at=created,
    )


INSERT_ROLE_DEFAULTS = (
    _insert_role_simply(ROLE_SLUG_OWNER, lock=True),
    _insert_role_simply(ROLE_SLUG_MAINTAINER),
    _insert_role_simply(ROLE_SLUG_DEVELOPER),
    _insert_role_simply(ROLE_SLUG_REPORTER),
    _insert_role_simply(ROLE_SLUG_GUEST),
)


def get_update_role_query_by_uid(
    uid: int,
    slug: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    extra: Optional[Any] = None,
    hidden: Optional[bool] = None,
    lock: Optional[bool] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    updated = updated_at if updated_at else tznow()
    builder = UpdateBuilder(
        if_none_skip=True,
        slug=slug,
        name=name,
        description=description,
        extra=extra,
        hidden=hidden,
        lock=lock,
        updated_at=updated,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_ROLE)
