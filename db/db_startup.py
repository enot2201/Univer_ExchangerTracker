from db.connection.connect import connection
from loguru import logger
from asyncpg import Connection
from conf.config import ConfigDatabase


async def startup_database():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS trade_info
(
    id SERIAL PRIMARY KEY,
    url text COLLATE pg_catalog."default" NOT NULL,
    currency_pair text COLLATE pg_catalog."default" NOT NULL,
    task_type text COLLATE pg_catalog."default" NOT NULL,
    wrapper_type text COLLATE pg_catalog."default" NOT NULL
);
    """
        insert_query = """
                INSERT INTO trade_info (
    url, currency_pair, task_type, wrapper_type) VALUES (
    'wss://stream.binance.com:9443/ws/btcusdt@trade', 'bitcoin-usd', 
    'parser_service.binance.task:BinanceTask', 'binance');
INSERT INTO trade_info (
    url, currency_pair, task_type, wrapper_type) VALUES (
    'wss://stream.binance.com:9443/ws/ethusdt@trade', 'tether-usd', 
    'parser_service.binance.task:BinanceTask', 'binance');
INSERT INTO trade_info (
    url, currency_pair, task_type, wrapper_type) VALUES (
    'wss://stream.binance.com:9443/ws/trxusdt@trade', 'tron-usd', 
    'parser_service.binance.task:BinanceTask', 'binance');
INSERT INTO trade_info (
    url, currency_pair, task_type, wrapper_type) VALUES (
    'https://api.coingecko.com/api/v3/simple/price', 'bitcoin,ethereum,tether,tron-rub,usd', 
    'parser_service.coingeko.task:CoingeckoTask', 'coingecko');
                """

        conn = await connection()
        await conn.execute(query)
        await conn.execute(insert_query)
        logger.info("Database create insert successful")
        await conn.close()
    except Exception as error:
        logger.error(f"Trouble with execute query {error}")



