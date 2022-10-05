from email import message
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from models import UserModel
from db import db
from schema import UserSchema
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

blp = Blueprint("Users", "users" )


@blp.route("/register")
class Register:

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(500, message="User With That username Already Exists!")
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit
        return {"message": "User Created"}


@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "User Is Deleted"}


@blp.route("/user-login")
class Login(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            username = user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"] and user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(401, message="Invalid Credentials")