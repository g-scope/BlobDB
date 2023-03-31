from peewee import *

# TODO relocate this to another location for configuration reference/switching.
database = SqliteDatabase("database.sqlite")

class BaseModel(Model):
    class Meta:
        database = database