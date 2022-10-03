from email import message
from pydoc import describe
import uuid
from flask import request, session
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, db
from models.items import *
from schema import ItemSchema, UpdateItemSchema
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
    @itm.arguments(ItemSchema)
    @itm.response(202, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit
        return {"Message": "Item Deleted"}

    @itm.arguments(UpdateItemSchema)
    @itm.response(200, ItemSchema)
    def put(self, item_id, item_data):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)

            db.session.add(item)
            db.session.commit
        return item


@itm.route("/list-items")
class ListItem(MethodView):
    @itm.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()