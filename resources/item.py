from email import message
from pydoc import describe
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, db
from models.items import ItemModel
from schema import ItemSchema
from sqlalchemy.exc import SQLAlchemyError 


itm = Blueprint("Items", "items", description="Operation on item")


@itm.route("/add-item")
class AddItem(MethodView):

    @itm.arguments(ItemSchema)
    @itm.response(201, ItemSchema)
    def post(self, data):
        item = ItemModel(**data)
        try:
            db.session.add(item)
            db.session.commit
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting item in database")


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