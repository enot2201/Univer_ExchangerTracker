from parser_service.base.base import BaseTask


class HttpTaskBase(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(BaseTask, self).__init__(*args, **kwargs)

    async def connection(self) -> None:
        return None
