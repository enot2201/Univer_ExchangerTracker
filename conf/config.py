from decouple import config


class ConfigDatabase(object):
    DB_HOST = config('DB_HOST', default='localhost')
    DB_PORT = config('DB_PORT', default='5555')
    DB_NAME = config('DB_NAME', default='ratetracker')
    DB_USER = config('DB_USER', default='postgres')
    DB_PASSWORD = config('DB_PASSWORD', default='8521946733')
    CONNECT_INFO_FIELD = config('CONNECT_INFO_FIELD', default='trade_info')


class RabbitMQ(object):
    BROKER_URL = config('BROKER_URL', default='amqp://guest:guest@localhost//')
    arguments = {
        'x-max-length': 1
    }


class Coingecko(object):
    API_KEY = config('API_KEY', default='')

class ReddisCache(object):
    REDIS_URL = config('REDIS_URL', default='localhost')
    REDIS_PORT = config('REDIS_PORT', default='6379')

