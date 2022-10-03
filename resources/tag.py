from email import message
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import ItemModel, StoreModel, TagModel
from schema import TagSchema


tg = Blueprint("Tags", "tags", description="Operations on tags")


@tg.route("/store/<string: store_id>/tag")
class TagsInStore(MethodView):
    @tg.response(TagSchema)
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


@tg.route("tag/<sting:tag_id>")
class Tag(MethodView):

    @tg.response(200, TagSchema):
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag