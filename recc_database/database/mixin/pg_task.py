# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Dict, List, Optional

from recc_database.chrono.datetime import tznow
from recc_database.database.mixin._pg_base import PgBase
from recc_database.database.query.task import (
    DELETE_TASK_BY_PROJECT_UID_AND_SLUG,
    DELETE_TASK_BY_UID,
    INSERT_TASK,
    SELECT_TASK_BY_FULLPATH,
    SELECT_TASK_BY_PROJECT_ID,
    SELECT_TASK_BY_PROJECT_ID_AND_SLUG,
    SELECT_TASK_BY_UID,
    SELECT_TASK_UID_BY_FULLPATH,
    SELECT_TASK_UID_BY_PROJECT_ID_AND_SLUG,
    UPDATE_TASK_DESCRIPTION_BY_PROJECT_UID_AND_SLUG,
    UPDATE_TASK_DESCRIPTION_BY_UID,
    UPDATE_TASK_EXTRA_BY_PROJECT_UID_AND_SLUG,
    UPDATE_TASK_EXTRA_BY_UID,
    UPDATE_TASK_KEYS_BY_PROJECT_UID_AND_SLUG,
    UPDATE_TASK_KEYS_BY_UID,
    get_update_task_query_by_uid,
)
from recc_database.packet.task import Task


class PgTask(PgBase):
    async def insert_task(
        self,
        project_uid: int,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        rpc_address: Optional[str] = None,
        auth_algorithm: Optional[str] = None,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else tznow()
        return await self.column(
            int,
            INSERT_TASK,
            project_uid,
            slug,
            name,
            description,
            extra,
            rpc_address,
            auth_algorithm,
            private_key,
            public_key,
            maximum_restart_count,
            numa_memory_nodes,
            base_image_name,
            publish_ports,
            created,
        )

    async def update_task_description_by_uid(
        self,
        uid: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(UPDATE_TASK_DESCRIPTION_BY_UID, uid, description, updated)

    async def update_task_description_by_slug(
        self,
        project_uid: int,
        slug: str,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(
            UPDATE_TASK_DESCRIPTION_BY_PROJECT_UID_AND_SLUG,
            project_uid,
            slug,
            description,
            updated,
        )

    async def update_task_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(UPDATE_TASK_EXTRA_BY_UID, uid, extra, updated)

    async def update_task_extra_by_slug(
        self,
        project_uid: int,
        slug: str,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(
            UPDATE_TASK_EXTRA_BY_PROJECT_UID_AND_SLUG,
            project_uid,
            slug,
            extra,
            updated,
        )

    async def update_task_keys_by_uid(
        self,
        uid: int,
        auth_algorithm: str,
        private_key: str,
        public_key: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(
            UPDATE_TASK_KEYS_BY_UID,
            uid,
            auth_algorithm,
            private_key,
            public_key,
            updated,
        )

    async def update_task_keys_by_slug(
        self,
        project_uid: int,
        slug: str,
        auth_algorithm: str,
        private_key: str,
        public_key: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(
            UPDATE_TASK_KEYS_BY_PROJECT_UID_AND_SLUG,
            project_uid,
            slug,
            auth_algorithm,
            private_key,
            public_key,
            updated,
        )

    async def update_task_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        rpc_address: Optional[str] = None,
        auth_algorithm: Optional[str] = None,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        query, args = get_update_task_query_by_uid(
            uid=uid,
            slug=slug,
            name=name,
            description=description,
            extra=extra,
            rpc_address=rpc_address,
            auth_algorithm=auth_algorithm,
            private_key=private_key,
            public_key=public_key,
            maximum_restart_count=maximum_restart_count,
            numa_memory_nodes=numa_memory_nodes,
            base_image_name=base_image_name,
            publish_ports=publish_ports,
            updated_at=updated,
        )
        await self.execute(query, *args)

    async def delete_task_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_TASK_BY_UID, uid)

    async def delete_task_by_slug(self, project_uid: int, slug: str) -> None:
        await self.execute(DELETE_TASK_BY_PROJECT_UID_AND_SLUG, project_uid, slug)

    async def select_task_by_uid(self, uid: int) -> Task:
        return await self.row(Task, SELECT_TASK_BY_UID, uid)

    async def select_task_by_slug(self, project_uid: int, slug: str) -> Task:
        return await self.row(
            Task,
            SELECT_TASK_BY_PROJECT_ID_AND_SLUG,
            project_uid,
            slug,
        )

    async def select_task_uid_by_slug(self, project_uid: int, slug: str) -> int:
        return await self.column(
            int,
            SELECT_TASK_UID_BY_PROJECT_ID_AND_SLUG,
            project_uid,
            slug,
        )

    async def select_task_by_project_uid(self, project_uid: int) -> List[Task]:
        return await self.rows(Task, SELECT_TASK_BY_PROJECT_ID, project_uid)

    async def select_task_by_fullpath(
        self, group_slug: str, project_slug: str, task_slug: str
    ) -> Task:
        return await self.row(
            Task,
            SELECT_TASK_BY_FULLPATH,
            group_slug,
            project_slug,
            task_slug,
        )

    async def select_task_uid_by_fullpath(
        self, group_slug: str, project_slug: str, task_slug: str
    ) -> int:
        return await self.column(
            int,
            SELECT_TASK_UID_BY_FULLPATH,
            group_slug,
            project_slug,
            task_slug,
        )
