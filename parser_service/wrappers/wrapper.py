import websockets
from websockets import WebSocketClientProtocol
from parser_service.wrappers.base import BaseWrapper
from loguru import logger
import asyncio
from db.connect_info.get.get import get_connection_info
from db.connect_info.schema.get.connection_info import ConnectionInfo
from parser_service.base.base import BaseTask
from importlib import import_module
from rabbit.queue.get import get_queue_name
from rabbit.queue.create import CreateQueue
import aio_pika
import json




class TaskWrapper(BaseWrapper):

    def __init__(self, *args, **kwargs):
        super(TaskWrapper, self).__init__()
        self.creator_queue = CreateQueue()

    async def task(self, instance: BaseTask, ws: WebSocketClientProtocol, channel: str):
        """Queue - очередь на брокере"""
        logger.info(f"Starting task: {instance}")
        reconnect_count = 0
        try:
            while True:
                data = await instance.execute(ws=ws)
                logger.debug(data)
                # await channel.default_exchange.publish(
                #     aio_pika.Message(body=price),
                #     routing_key='my_queue'
                # )
                for key, value in data["data"].items():
                    queue = self.creator_queue.queue_dict.get(key)
                    if queue is not None:
                        message = aio_pika.Message(body=json.dumps({queue.name.replace("/", "-"):
                                                                        {"value": float(value),
                                                                         "exchanger": instance.exchanger,
                                                                         "direction":
                                                                             queue.name.replace("/", "-")}}).encode())

                        await queue.channel.default_exchange.publish(message=message, routing_key=queue.name)
                await asyncio.sleep(5)
        except websockets.exceptions.WebSocketException as error:
            reconnect_count += 1
            logger.warning(f"Reconnecting \n try {reconnect_count}")
            ws = await instance.connection()
            await self.task(instance=instance, ws=ws, channel=channel)
            logger.warning(f"Reconnecting try {reconnect_count} failed")
            if reconnect_count == 10:
                logger.critical(f"Reconnecting failed raise Exception {error}")
                raise Exception(f"Reconnecting error")
        except Exception as error:
            logger.error(f"Unknown error {error}")

    async def create_task_classes(self) -> list[BaseTask]:

        instances = await self.preproccess()
        tasks = []
        for instance in instances:
            task = self.get_class_instance(instance.task_type)
            task_instance = task(url=instance.url, currency_pair=instance.currency_pair,
                                 channel=await self.creator_queue.create(instance), exchanger=instance.wrapper_type)
            tasks.append(task_instance)
        return tasks

        # return [BinanceTask(enpoints="BTC-USDT", url="wss://stream.binance.com:9443/ws/btcusdt@trade")]

    async def task_creation(self, *args, **kwargs) -> list:
        tasks = []
        for task in await self.create_task_classes():
            ws = await task.connection()
            tasks.append(self.task(instance=task, ws=ws, channel="test"))

        return tasks

    async def task_startup(self):
        logger.info("Starting parser service")
        tasks = await self.task_creation()
        await asyncio.gather(*tasks)

    async def preproccess(self) -> list[ConnectionInfo]:
        instances = await get_connection_info()
        logger.info("Prepsocess service: {}".format(instances))
        return instances

    @classmethod
    def get_class_instance(cls, path: str) -> object:
        module_name, class_name = path.rsplit(":", 1)
        module = import_module(module_name)
        return getattr(module, class_name)



