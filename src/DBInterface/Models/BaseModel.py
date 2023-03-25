from peewee import *

database = SqliteDatabase("database.sqlite")

class BaseModel(Model):
    class Meta:
        database = database