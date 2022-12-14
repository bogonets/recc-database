# -*- coding: utf-8 -*-

from datetime import datetime
from functools import lru_cache, reduce
from typing import Optional

from recc_database.chrono.datetime import tznow
from recc_database.database.mixin._pg_base import PgBase  # noqa
from recc_database.database.mixin.pg_group import PgGroup
from recc_database.database.mixin.pg_group_member import PgGroupMember
from recc_database.database.mixin.pg_info import PgInfo
from recc_database.database.mixin.pg_permission import PgPermission
from recc_database.database.mixin.pg_pip import PgPip
from recc_database.database.mixin.pg_project import PgProject
from recc_database.database.mixin.pg_project_member import PgProjectMember
from recc_database.database.mixin.pg_role import PgRole
from recc_database.database.mixin.pg_role_permission import PgRolePermission
from recc_database.database.mixin.pg_task import PgTask
from recc_database.database.mixin.pg_user import PgUser
from recc_database.database.mixin.pg_user_info import PgUserInfo
from recc_database.database.query.create.functions import (
    CREATE_FUNCTIONS,
    DROP_FUNCTIONS,
)
from recc_database.database.query.create.indices import CREATE_INDICES, DROP_INDICES
from recc_database.database.query.create.tables import CREATE_TABLES, DROP_TABLES
from recc_database.database.query.create.views import CREATE_VIEWS, DROP_VIEWS
from recc_database.database.query.info import (
    EXISTS_INFO_BY_KEY,
    INSERT_INFO,
    SELECT_INFO_UPDATED_AT_BY_KEY,
)
from recc_database.database.query.permission import INSERT_PERMISSION_DEFAULTS
from recc_database.database.query.role import INSERT_ROLE_DEFAULTS
from recc_database.database.query.role_permission import DEFAULT_INSERT_ROLE_PERMISSIONS
from recc_database.variables.database import INFO_KEY_RECC_DB_VERSION


@lru_cache
def version() -> str:
    # [IMPORTANT] Avoid 'circular import' issues
    from recc_database import __version__

    return __version__


def _merge_queries(*args: str) -> str:
    return reduce(lambda x, y: x + y, args)


class PgDb(
    PgGroup,
    PgGroupMember,
    PgInfo,
    PgPermission,
    PgPip,
    PgProject,
    PgProjectMember,
    PgRole,
    PgRolePermission,
    PgTask,
    PgUser,
    PgUserInfo,
):
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        pw: Optional[str] = None,
        name: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self._pool = None
        self._host = host
        self._port = port
        self._user = user
        self._pw = pw
        self._name = name
        self._timeout = timeout

    def is_open(self) -> bool:
        return PgBase.is_open(self)

    async def open(self) -> None:
        await PgBase.open(self)

    async def close(self) -> None:
        await PgBase.close(self)

    async def drop_database(self) -> None:
        await PgBase.drop_database(self)

    async def create_tables(self) -> None:
        async with self.conn() as conn:
            async with conn.transaction():
                create_tables = _merge_queries(*CREATE_TABLES)
                await conn.execute(create_tables)

                create_indices = _merge_queries(*CREATE_INDICES)
                await conn.execute(create_indices)

                create_views = _merge_queries(*CREATE_VIEWS)
                await conn.execute(create_views)

                create_functions = _merge_queries(*CREATE_FUNCTIONS)
                await conn.execute(create_functions)

                exists_db_version = await conn.fetchval(
                    EXISTS_INFO_BY_KEY, INFO_KEY_RECC_DB_VERSION
                )
                if exists_db_version:
                    db_version_updated_at = await conn.fetchval(
                        SELECT_INFO_UPDATED_AT_BY_KEY, INFO_KEY_RECC_DB_VERSION
                    )
                    assert isinstance(db_version_updated_at, datetime)
                    # logger.info(
                    #   f"Already database updated at: {db_version_updated_at}"
                    # )
                    return

                insert_perms = _merge_queries(*INSERT_PERMISSION_DEFAULTS)
                await conn.execute(insert_perms)

                insert_roles = _merge_queries(*INSERT_ROLE_DEFAULTS)
                await conn.execute(insert_roles)

                insert_role_perms = _merge_queries(*DEFAULT_INSERT_ROLE_PERMISSIONS)
                await conn.execute(insert_role_perms)

                await conn.execute(
                    INSERT_INFO,
                    INFO_KEY_RECC_DB_VERSION,
                    version(),
                    tznow(),
                )
                # logger.info("Database initialization complete")

    async def drop_tables(self) -> None:
        all_drop = DROP_TABLES + DROP_INDICES + DROP_VIEWS + DROP_FUNCTIONS
        all_drop_reverse = all_drop[::-1]
        queries = _merge_queries(*all_drop_reverse)
        assert isinstance(queries, str)
        await self.execute(queries)
        # logger.info("All tables have been successfully dropped")
