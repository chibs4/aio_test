from typing import Dict, List
from datetime import date
from fastapi import FastAPI, HTTPException
from models import Rates, Dates, CargoTypes
from schemas import Rates_Pydantic,Dates_Pydantic,CargoTypes_Pydantic
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
import json


app = FastAPI(title="Тестовое задание")


class Cargo(BaseModel):
    cargo_type: str
    rate: str


class Data(BaseModel):
    data: Dict[str, List[Cargo]]


@app.get("/rates", response_model=List[Rates_Pydantic])
async def get_rates():
    return await Rates_Pydantic.from_queryset(Rates.all())


@app.post("/add-rates")
async def create_rates(data: Data):
    for date in data.data.keys():
        date_obj, created = await Dates.get_or_create(date=date)
        await Dates_Pydantic.from_tortoise_orm(date_obj)
        for rate in data.data.values():
            for cargo in rate:
                cargo_obj, created = await CargoTypes.get_or_create(type=cargo.cargo_type)
                await CargoTypes_Pydantic.from_tortoise_orm(cargo_obj)
                rate_obj, created = await Rates.get_or_create(date_id=date_obj.id, type_id=cargo_obj.id, rate=cargo.rate)
                await Rates_Pydantic.from_tortoise_orm(rate_obj)


@app.get("/get-price")
async def get_price(d:date, t: str, p:int):
    res = await Rates.filter(type__type=t, date__date=d).first()
    try:
        return res.rate*p
    except AttributeError:
        raise HTTPException(status_code=404, detail="Rate not found")


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event("startup")
async def startup_event():
    with open('rates.json', 'r') as f:
        await create_rates(Data(**json.load(f)))


