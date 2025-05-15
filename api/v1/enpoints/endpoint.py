from fastapi import Query, HTTPException
from fastapi import HTTPException

from cahce.get.get import get_data
from fastapi import APIRouter
import json
from api.v1.schema.currency_pair import Course, CurrencyPairData

router = APIRouter(prefix="/v1")


@router.get("/currency_pair/")
async def get_currency_pair(currency_pair: str = Query(...)) -> CurrencyPairData:
    data = await get_data(currency_pair)
    if data is None:
        raise HTTPException(status_code=400, detail="Pair not found")
    data = eval(data)
    response = CurrencyPairData(exchanger=data["exchanger"], courses=[Course(direction=data["direction"], value=data["value"])])
    return response
