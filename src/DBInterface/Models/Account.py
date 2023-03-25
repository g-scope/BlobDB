from peewee import *
from DBInterface.Models.BaseModel import BaseModel

class Account(BaseModel):
    username = CharField(unique=True)
    password = TextField(default="")
    email = TextField(default="")
    
    salt = TextField(default="")
    
    nonce = TextField(default="")
    data = TextField(default="")