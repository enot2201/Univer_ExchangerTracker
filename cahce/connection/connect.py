import asyncio_redis
from conf.config import ReddisCache
from loguru import logger


async def connection():
    logger.info("Connecting to redis...")
    r = await asyncio_redis.Connection.create(ReddisCache.REDIS_URL)
    logger.info("Connected to redis!")
    return r
