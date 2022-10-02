from email import message
from pydoc import describe
from sqlite3 import IntegrityError
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, store
from schema import StoreSchema
from models.store import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("stores", __name__, description="Operations on store")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(slef, store_id):
        try:
            return store[store_id]
        except KeyError:
            abort(404, message="Store Not Found")

    def delete(self, store_id):
        try:
            del store[store_id]
            return {"message": "store deleted"}
        except KeyError:
            abort(404, message="Store Not Found")


@blp.route("/add-store")
class AddStore(MethodView):

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, data):
        store = StoreModel(**data)
        try:
            db.session.add(store)
        except IntegrityError:
            abort (400, message="A Store with name is already exist")
        except SQLAlchemyError:
            abort(500, message="an error occurred the store ")
        return store