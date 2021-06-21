from tortoise import fields, models
from tortoise import Tortoise
from datetime import datetime


class Rates(models.Model):
    id = fields.IntField(pk=True)
    date = fields.ForeignKeyField('models.Dates')
    type = fields.ForeignKeyField('models.CargoTypes')
    rate = fields.FloatField()


class Dates(models.Model):
    id = fields.IntField(pk=True)
    date = fields.DateField(unique=True)


class CargoTypes(models.Model):
    id = fields.IntField(pk=True)
    type = fields.CharField(unique=True, max_length=100)


Tortoise.init_models(['models'], "models")
