from email import message
from pydoc import describe
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schema import ItemSchema



itm = Blueprint("Items", "items", description="Operation on item")


@itm.route("/add-item")
class AddItem(MethodView):

    @itm.arguments(ItemSchema)
    def post(self, data):
        # data = request.get_json()
        if data is None:
            abort(505, message="Missing Data")
        item_id = uuid.uuid4().hex
        items = {**data, "id": item_id}
        return data

@itm.route("/item/<string:item_id>")
class Item(MethodView):
    @itm.response(202, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item Doesn't Exist")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": f"{item_id} is Deleted"}
        except KeyError:
            abort(404, message="Item Is Not Define")