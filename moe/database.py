from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine

import moe.utils as utils

metadata = MetaData()

keys = Table(
    "keys",
    metadata,
    Column("name", String(), unique=True, nullable=False),
    Column("password_hash", String(), nullable=False),
    Column("visits", Integer, server_default="0", nullable=False)
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def begin():
    return create_async_engine('sqlite+aiosqlite:///.\\db.sqlite3', echo=True).begin()


async def sync():
    async with begin() as conn:
        await conn.run_sync(metadata.create_all)


async def create_key(key, password, salt):
    async with begin() as conn:
        if not (await conn.execute(select(True).where(keys.c.name == key))).scalar():
            password_hash = utils.hash_password(password, salt)
            await conn.execute(insert(keys).values(name=key, password_hash=password_hash))
            return password_hash


async def revoke_key(key, password, salt):
    async with begin() as conn:
        password_hash = utils.hash_password(password, salt)
        return (await conn.execute(
            delete(keys).where(and_(keys.c.name == key, keys.c.password_hash == password_hash)))).rowcount > 0


async def set_visits(key, value, password, salt):
    value = max(value, 0)
    async with begin() as conn:
        return (await conn.execute(update(keys).where(
            and_(keys.c.name == key, keys.c.password_hash == utils.hash_password(password, salt))).values(
            visits=value))).rowcount > 0


async def get_visits(key, do_inc):
    async with begin() as conn:
        result = (await conn.execute(select(keys.c.visits).where(keys.c.name == key))).scalar()
        if result is not None:
            if do_inc:
                result += 1
                await conn.execute(update(keys).where(keys.c.name == key).values(visits=result))
            return result
        return -1


async def check_password(key, password, salt):
    async with begin() as conn:
        return len((await conn.execute(
            select(keys).where(
                and_(keys.c.name == key, keys.c.password_hash == utils.hash_password(password, salt))
            ))).fetchall()) > 0


async def check_key(key):
    async with begin() as conn:
        return len((await conn.execute(
            select(keys).where(keys.c.name == key))).fetchall()) > 0
