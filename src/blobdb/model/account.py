from blobdb.model.base import BaseModel
from peewee import *

class AccountModel(BaseModel):
    username = TextField(unique=True,primary_key=True)
    password = TextField(default="")
    salt = TextField(default="")
    
    data = TextField(default="")
    nonce = TextField(default="")