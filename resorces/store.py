from email import message
from pydoc import describe
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, store
from schema import StoreSchema

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
    def post(self, data):
        # data = request.get_json()
        store_id = uuid.uuid4().hex
        store = {**data, "id": store_id}
        return store