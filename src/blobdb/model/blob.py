from blobdb.model.base import BaseModel
from peewee import *

class BlobModel(BaseModel):
    bid = TextField(unique=True, primary_key=True)
    data = TextField(default="")