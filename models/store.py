from enum import unique
from db import db

class StoreModel(db.Model):
    __table_name = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    