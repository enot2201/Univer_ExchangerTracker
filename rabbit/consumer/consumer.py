import aio_pika
from rabbit.queue.create import CreateQueue
from db.connect_info.get.get import get_connection_info
from conf.config import RabbitMQ
from loguru import logger
from cahce.connection.connect import connection
from cahce.set.set import set_data
import json
class Consumer:
    def __init__(self):
        self.queues = []
        self.queue_creator = CreateQueue()
        self.connect_redis = None
        logger.info("Consumer initialized")





    async def get_queues_name(self):
        connections_info = await get_connection_info()
        queues = []
        for con_info in connections_info:
            queues.append(self.queue_creator.create_queue_name(con_info))
        return queues

    async def create_queue(self):
        connection = await aio_pika.connect_robust(RabbitMQ.BROKER_URL)
        channel = await connection.channel()
        names_collection = await self.get_queues_name()
        for names in names_collection:
            for name in names:
                self.queues.append(await channel.get_queue(name))

    async def callback(self, message: aio_pika.Message):
        data = message.body.decode()
        data = json.loads(data)
        key = next(iter(data))
        value = str(data[key])
        await set_data(key=key, value=value, conn=self.connect_redis)
        logger.debug("Received message: {}".format(message.body.decode()))



    async def start(self):
        logger.info("Starting consumer")
        self.connect_redis = await connection()
        logger.info("Connection redis established")
        await self.create_queue()
        for queue in self.queues:
            await queue.consume(self.callback)
