from pydantic import BaseModel


class Course(BaseModel):
    direction: str
    value: float


class CurrencyPairData(BaseModel):
    exchanger: str
    courses: list[Course]
