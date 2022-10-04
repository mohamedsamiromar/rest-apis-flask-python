from email import message
from operator import gt
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import  StoreModel, TagModel
from models.items import ItemModel
from schema import TagSchema, TagAndItemSchema


tg = Blueprint("Tags", "tags", description="Operations on tags")


@tg.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @tg.response(202, TagSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()


    @tg.arguments(TagSchema)
    @tg.response(202, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(
            TagModel.store_id == store_id, TagModel.name == tag_data["name"]
            ).first():
            abort(
                400, message="Tag with that name already exist in that store"
            )
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e)
                )
        return tag


@tg.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @tg.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag


@tg.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagToItem(MethodView):

    @tg.response(200, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting tag")
        return tag  
    

    @tg.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occurred while insert")
        return {"message": "Item removed from tag", "item": item, "tag": tag}


@tg.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @tg.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        try:
            db.session.add(tag)
            db.session.commit
        except SQLAlchemyError:
            abort(
                500, message="Error Occurred while get tag"
            )
    

    @tg.response(202,
     description="Delete a Tag from item is tagged  it.",
     example={"message": "Tag Deleted"})

    @tg.response(404, description="Tag Not Found")
    @tg.alt_response(400, description="Return if the tag is assigned to one or more items, In this case, the tag is not  deleted.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag:
            db.session.delete(tag)
            db.session.commit
            return {"message": "Tag Deleted"}
        abort(400, message="Could Not Deleted Tag, Make Sure the Tag is assigned to one or more items, In this case, the tag is not  deleted.")