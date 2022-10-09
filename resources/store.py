from sqlite3 import IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import StoreSchema, UpdateStoreSchema
from models.store import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
blp = Blueprint("stores", __name__, description="Operations on store")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit
        return {"message": "Store Has Been Deleted"}
    
    @jwt_required()
    @blp.arguments(UpdateStoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get_or_404(store_id)
        if store:
            store.name = store_data['name']
        else:
            store = StoreModel(**store_data)
            db.session.add(store)
            db.session.commit
        return store



@blp.route("/add-store")
class AddStore(MethodView):

    @jwt_required()
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