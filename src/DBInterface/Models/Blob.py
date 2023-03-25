from peewee import *
from DBInterface.Models.BaseModel import BaseModel

class Blob(BaseModel):
    bid = TextField(unique=True,primary_key=True)
    blob = TextField()