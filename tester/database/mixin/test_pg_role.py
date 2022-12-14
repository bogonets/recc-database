# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from unittest import main

from recc_database.variables.database import ROLE_SLUG_OWNER, ROLE_UID_OWNER
from tester.postgresql_test_case import PostgresqlTestCase


class PgRoleTestCase(PostgresqlTestCase):
    async def test_owner_role(self):
        owner_uid = await self.db.select_role_uid_by_slug(ROLE_SLUG_OWNER)
        self.assertEqual(ROLE_UID_OWNER, owner_uid)

    async def test_create_and_get(self):
        slug1 = "role1"
        slug2 = "role2"
        desc1 = "desc1"
        desc2 = "desc2"
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        created_at2 = datetime.now().astimezone() + timedelta(days=2)
        result1_uid = await self.db.insert_role(
            slug1,
            description=desc1,
            created_at=created_at1,
        )
        result2_uid = await self.db.insert_role(
            slug2,
            description=desc2,
            created_at=created_at2,
        )
        role1_uid = await self.db.select_role_uid_by_slug(slug1)
        role2_uid = await self.db.select_role_uid_by_slug(slug2)
        self.assertEqual(result1_uid, role1_uid)
        self.assertEqual(result2_uid, role2_uid)
        role1 = await self.db.select_role_by_uid(role1_uid)
        role2 = await self.db.select_role_by_uid(role2_uid)
        self.assertEqual(slug1, role1.slug)
        self.assertEqual(slug2, role2.slug)
        self.assertIsNone(role1.name)
        self.assertIsNone(role2.name)
        self.assertEqual(desc1, role1.description)
        self.assertEqual(desc2, role2.description)
        self.assertFalse(role1.hidden)
        self.assertFalse(role2.hidden)
        self.assertFalse(role1.lock)
        self.assertFalse(role2.lock)
        self.assertIsNone(role1.extra)
        self.assertIsNone(role2.extra)
        self.assertEqual(created_at1, role1.created_at)
        self.assertEqual(created_at2, role2.created_at)
        self.assertEqual(created_at1, role1.updated_at)
        self.assertEqual(created_at2, role2.updated_at)

        role1_uid = role1.uid
        role2_uid = role2.uid
        self.assertNotEqual(role1_uid, role2_uid)

    async def test_update_role(self):
        slug1 = "role1"
        await self.db.insert_role(slug1)
        role1_uid = await self.db.select_role_uid_by_slug(slug1)
        role1 = await self.db.select_role_by_uid(role1_uid)
        self.assertEqual(slug1, role1.slug)
        self.assertIsNone(role1.name)
        self.assertIsNone(role1.description)
        self.assertIsNone(role1.extra)
        self.assertIsNotNone(role1.created_at)
        self.assertIsNotNone(role1.updated_at)
        self.assertEqual(role1.created_at, role1.updated_at)

        updated_slug = "role2"
        updated_desc = "desc2"
        updated_extra = {"A": 65, "B": 66}
        updated_at = datetime.now().astimezone() + timedelta(days=7)
        await self.db.update_role_by_uid(
            role1.uid,
            slug=updated_slug,
            description=updated_desc,
            extra=updated_extra,
            updated_at=updated_at,
        )
        updated_role1 = await self.db.select_role_by_uid(role1.uid)
        self.assertEqual(updated_slug, updated_role1.slug)
        self.assertIsNone(updated_role1.name)
        self.assertEqual(updated_desc, updated_role1.description)
        self.assertEqual(updated_extra, updated_role1.extra)
        self.assertEqual(updated_at, updated_role1.updated_at)
        self.assertFalse(updated_role1.hidden)
        self.assertFalse(updated_role1.lock)

    async def test_delete(self):
        role1_uid = await self.db.insert_role("role1")

        roles1 = await self.db.select_role_all()
        roles1_ids = [g.uid for g in roles1]
        self.assertIn(role1_uid, roles1_ids)

        await self.db.delete_role_by_uid(role1_uid)

        roles2 = await self.db.select_role_all()
        roles2_ids = [g.uid for g in roles2]
        self.assertNotIn(role1_uid, roles2_ids)

    async def test_group_member_role(self):
        role1_uid = await self.db.insert_role("role1")

        user1_uid = await self.db.insert_user("user1", "pass", "salt")
        group1_uid = await self.db.insert_group("group1")
        await self.db.insert_group_member(group1_uid, user1_uid, role1_uid)

        role = await self.db.select_role_by_user_uid_and_group_uid(
            user1_uid, group1_uid
        )
        self.assertEqual(role1_uid, role.uid)

    async def test_project_member_role(self):
        role1_uid = await self.db.insert_role("role1")
        role2_uid = await self.db.insert_role("role2")

        user1_uid = await self.db.insert_user("user1", "pass", "salt")

        group1_uid = await self.db.insert_group("group1")
        await self.db.insert_group_member(group1_uid, user1_uid, role1_uid)

        project1_uid = await self.db.insert_project(group1_uid, "project1")
        await self.db.insert_project_member(project1_uid, user1_uid, role2_uid)

        role = await self.db.select_role_by_user_uid_and_project_uid(
            user1_uid, project1_uid
        )
        self.assertEqual(role2_uid, role.uid)


if __name__ == "__main__":
    main()
