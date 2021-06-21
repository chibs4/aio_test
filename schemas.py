from tortoise.contrib.pydantic import pydantic_model_creator
from models import Rates,Dates,CargoTypes


Rates_Pydantic = pydantic_model_creator(Rates, name="rates")
Dates_Pydantic = pydantic_model_creator(Dates, name="dates")
CargoTypes_Pydantic = pydantic_model_creator(CargoTypes, name="cargo_types")
