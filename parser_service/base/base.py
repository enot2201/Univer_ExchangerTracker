from abc import ABC, abstractmethod
from datetime import datetime


class BaseTask(ABC):

    def __init__(self, *args, **kwargs):
        """Передаются данные для инициализации задачи. Реализация зависит от таргет функции execute"""
        self.last_update: datetime | None = None
        self.reconnect_count: int = 0

        self.currency_pair: str | None = kwargs.get('currency_pair', None)
        self.exchanger: str = kwargs.get('exchanger')

    @abstractmethod
    async def execute(self, *args, **kwargs) -> dict:
        """Execute функцию нужна для обнволения курса"""
        pass

    def benchmark(self):
        """Вычисление таймингов обновления"""
        if self.last_update is None:
            return 0
        return (datetime.now() - self.last_update).seconds

