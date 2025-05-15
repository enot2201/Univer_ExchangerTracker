import traceback

import asyncpg
from loguru import logger
from conf.config import ConfigDatabase


async def connection() -> asyncpg.Connection:
    try:
        conn = await asyncpg.connect(
            user=ConfigDatabase.DB_USER,
            password=ConfigDatabase.DB_PASSWORD,
            database=ConfigDatabase.DB_NAME,
            host=ConfigDatabase.DB_HOST,
        )
        return conn
    except Exception as error:
        logger.critical("Connection bd error", error)
        logger.critical(f"{ConfigDatabase.DB_HOST}:{ConfigDatabase.DB_PORT} - {ConfigDatabase.DB_USER} - "
                        f"{ConfigDatabase.DB_PASSWORD} - {ConfigDatabase.DB_NAME} - {error}")



