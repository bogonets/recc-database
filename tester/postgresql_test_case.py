# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase

from recc_database.database.pg_db import PgDb


class PostgresqlTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        self.host = "localhost"
        self.port = 5432
        self.user = "recc"
        self.pw = "recc1234"
        self.name = "recc_db.test"
        self.db = PgDb(self.host, self.port, self.user, self.pw, self.name)

    async def asyncSetUp(self):
        await self.db.open()
        self.assertTrue(self.db.is_open())
        await self.db.drop_tables()
        await self.db.create_tables()

    async def asyncTearDown(self):
        await self.db.close()
        self.assertFalse(self.db.is_open())
