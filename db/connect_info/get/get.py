from db.connect_info.schema.get.connection_info import ConnectionInfo
from conf.config import ConfigDatabase
from db.connection.connect import connection
from db.db_startup import startup_database
from asyncpg.exceptions import UndefinedTableError
from loguru import logger


async def get_connection_info():
    try:

        query = """SELECT id, url, currency_pair, task_type, wrapper_type FROM trade_info"""
        conn = await connection()
        res = await conn.fetch(query)
        instance_list = []
        for instance_data in res:
            instance_list.append(ConnectionInfo(**instance_data))
        return instance_list
    except UndefinedTableError as error:
        logger.info("UndefinedTableError: %s", error)
        await startup_database()
        await get_connection_info()