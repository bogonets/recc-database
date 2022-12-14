# -*- coding: utf-8 -*-

from recc_database.variables.database import TABLE_INFO, VIEW_INFO_DB_VERSION

INSERT_INFO = f"""
INSERT INTO {TABLE_INFO} (
    key,
    value,
    created_at,
    updated_at
) VALUES (
    $1, $2, $3, $3
);
"""

UPSERT_INFO = f"""
INSERT INTO {TABLE_INFO} (
    key,
    value,
    created_at,
    updated_at
) VALUES (
    $1, $2, $3, $3
) ON CONFLICT (
    key
) DO UPDATE SET
    value=$2,
    updated_at=$3;
"""

UPDATE_INFO_VALUE_BY_KEY = f"""
UPDATE {TABLE_INFO}
SET value=$2, updated_at=$3
WHERE key=$1;
"""

DELETE_INFO_BY_KEY = f"""
DELETE FROM {TABLE_INFO}
WHERE key=$1;
"""

EXISTS_INFO_BY_KEY = f"""
SELECT EXISTS (
    SELECT *
    FROM {TABLE_INFO}
    WHERE key=$1
);
"""

SELECT_INFO_UPDATED_AT_BY_KEY = f"""
SELECT updated_at
FROM {TABLE_INFO}
WHERE key=$1;
"""

SELECT_INFO_BY_KEY = f"""
SELECT *
FROM {TABLE_INFO}
WHERE key=$1;
"""

SELECT_INFO_BY_KEY_LIKE = f"""
SELECT *
FROM {TABLE_INFO}
WHERE key LIKE $1;
"""

SELECT_INFO_ALL = f"""
SELECT *
FROM {TABLE_INFO};
"""

SELECT_INFO_DB_VERSION = f"""
SELECT version
FROM {VIEW_INFO_DB_VERSION};
"""
