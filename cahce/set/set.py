from asyncio_redis import Connection


async def set_data(key, value, conn: Connection) -> None:
    await conn.set(key, value)

