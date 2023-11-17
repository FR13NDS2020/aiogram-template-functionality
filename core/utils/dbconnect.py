import asyncpg
import psycopg_pool


class Request:
    # def __init__(self, connector: asyncpg.pool.Pool):  # asyncpg version
    def __init__(self, connector: psycopg_pool.AsyncConnectionPool.connection):  # psycopg Version
        self.connector = connector

    async def add_data(self, user_id, user_name):
        query = f"INSERT INTO datausers (user_id, user_name) VALUES ({user_id}, '{user_name}')" \
                f" ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        await self.connector.execute(query)
