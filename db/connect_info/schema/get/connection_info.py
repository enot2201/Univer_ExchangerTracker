from pydantic import BaseModel


class ConnectionInfo(BaseModel):
    id: int
    url: str
    currency_pair: str
    task_type: str
    wrapper_type: str
