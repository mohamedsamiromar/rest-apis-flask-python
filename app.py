from atexit import register
from flask import Flask, jsonify
from flask_smorest import Api
from resources.item import itm as ItemBluPrint
from resources.store import blp as StoreBluPrint
from resources.tag import tg as TagBluePrint
from resources.user import blp as UserBlueprint
from flask_jwt_extended import JWTManager
import secrets
import os
from db import db
from models import UserModel
from blocklist import BLOCKLIST
from flask_migrate import Migrate


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True 
    app.config["API_TITLE"] = "Store Rest API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]= "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "809925493099150565945117651761603124"

    """
    How generate secret key?
    - import secrets
    - run this in terminal secrets.SystemRandom().getrandbits(120)
      and will generate secret key :) 
    """

    db.init_app(app)
    migrate = Migrate(app=app, db=db)

    api = Api(app)
    jwt = JWTManager(app)

    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #   # look in the database and see weather the users is an admin 
    #   user  = UserModel.query.filter(id=identity)
    #   if user == "is_admin":
    #     return {"is_admin": True}
    #   return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The Token has been revoked.", "error": "Token revoked"}
            ),
            401
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "the toke is not fresh", 
                    "error": "fresh_token_required"}
            ),
            401
        )


    api.register_blueprint(ItemBluPrint)
    api.register_blueprint(StoreBluPrint)
    app.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBlueprint)

    return app
