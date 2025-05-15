from abc import ABC, abstractmethod

from parser_service.base.base import BaseTask


class BaseWrapper(ABC):

    def __init__(self):
        """При наследовании обязательно реализовывать"""

    # @abstractmethod
    # async def tasks_startup(self):
    #     """Запуск задач"""
    #     pass

    @abstractmethod
    def create_task_classes(self):
        """Создание классов"""
        pass

    @abstractmethod
    async def preproccess(self):
        """Получение ссылок из бд, символьной пары, всяких описаний, полный простор для творчества"""
        pass

    @abstractmethod
    async def task_creation(self, *args, **kwargs):
        """создание массива задач"""

    @abstractmethod
    async def task(self, *args, **kwargs):
        """Задача"""


    # @abstractmethod
    # async def message_broker(self, message):
    #     """Сообщение брокеру"""
    #     pass
    #
    # @abstractmethod
    # async def connect_broker(self):
    #     """Подключение к брокеру и создание очереди"""