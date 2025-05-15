import asyncio
from datetime import datetime

from conf.config import Coingecko
import aiohttp
from db.connect_info.schema.get.connection_info import ConnectionInfo
import json
from loguru import logger
from parser_service.http_task.base import HttpTaskBase
from rabbit.queue.get import get_queue_name

class CoingeckoTask(HttpTaskBase):
    logger.add("parshttp.log", rotation="500MB")

    def __init__(self, *args, **kwargs):
        super(HttpTaskBase, self).__init__(*args, **kwargs)
        self.coingecko_api_key = Coingecko.API_KEY
        self.url = kwargs.get('url')
        self.parsing_currency: list = []
        self.target_currency: list = []
        self.channel_base = ""
        self.routing_base = ""

    async def execute(self, *args, **kwargs) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                data = await response.json()
                if self.benchmark() > 5:
                    logger.warning(f"Time update: {self.benchmark()} for {self.currency_pair} is overtime")
                else:
                    logger.info(f"Time update: {self.benchmark()} {self.currency_pair}")
                self.last_update = datetime.now()
                return self.normalize(data)

    async def connection(self):
        """Создание урла для парсинга"""
        parsing_currency, target_currency = self.currency_pair.rsplit("-", 1)
        parsing_currency = parsing_currency.split(",")
        self.parsing_currency = parsing_currency.copy()
        target_currency = target_currency.split(",")
        self.target_currency = target_currency.copy()
        parsing_currency_str = "%2C".join(parsing_currency)
        target_currency_str = "%2C".join(target_currency)
        url = "".join([f"{self.url}?", f"ids={parsing_currency_str}&",
                        f"vs_currencies={target_currency_str}"])
        self.url = url
        return None

    def normalize(self, data: dict) -> dict:
        res = {"data": {}}
        for key, value in data.items():
            """Проходим по внешнему словарю"""
            for key_target, value_target in value.items():
                """Обход словаря с результатом"""
                res["data"].update({get_queue_name('-'.join([key, key_target])): value_target})
        return res


task = CoingeckoTask(url="https://api.coingecko.com/api/v3/simple/price", currency_pair="bitcoin,ethereum,tether,tron-rub,usd")



async def start():
    await task.connection()
    while True:
        await task.execute()
        await asyncio.sleep(3)
