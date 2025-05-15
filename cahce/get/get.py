from cahce.connection.connect import connection


async def get_data(key) -> str:
    conn = await connection()
    return await conn.get(key)
