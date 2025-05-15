from fastapi import FastAPI
import uvicorn
import aio_pika
from rabbit.consumer.consumer import Consumer
from api.v1.enpoints.endpoint import router as router_v1
from rabbit.queue.create import CreateQueue
from db.connect_info.get.get import get_connection_info
from db.db_startup import startup_database
from parser_service.wrappers.wrapper import TaskWrapper
import asyncio

app = FastAPI()


# @app.get("/")
# async def connect_to_binance_ws():
#     async with websockets.connection('wss://stream.binance.com:9443/ws/btcusdt@trade') as websocket:
#         while True:
#             data = await websocket.recv()
#             print(data)

@app.get("/")
async def index():
    return {"message": "hello"}

app.include_router(router_v1, prefix="/api")

async def consume(message: aio_pika.Message):
    async with message.process():
        print(message.body)



@app.on_event("startup")
async def startup():
    await startup_database()
    creator = CreateQueue()
    for info in await get_connection_info():
        await creator.create(info)
    consumer = Consumer()
    await consumer.start()






if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
