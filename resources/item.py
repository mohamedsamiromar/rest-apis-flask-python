from email import message
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import ItemModel
from schema import ItemSchema, UpdateItemSchema
from sqlalchemy.exc import SQLAlchemyError 
from flask_jwt_extended import jwt_required, get_jwt
itm = Blueprint("Items", "items", description="Operation on item")


@itm.route("/add-item")
class AddItem(MethodView):

    @jwt_required(fresh=True)
    @itm.arguments(ItemSchema)
    @itm.response(201, ItemSchema)
    def post(self, data):
        item = ItemModel(**data)
        try:
            db.session.add(item)
            db.session.commit
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting item in database")


@itm.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @itm.arguments(ItemSchema)
    @itm.response(202, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt
        if not jwt:
            abort(401, message="Admin privilege required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit
        return {"Message": "Item Deleted"}

    @jwt_required()
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