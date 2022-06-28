#!/usr/bin/env python

from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, get_identity

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.secret_key = "Sean"
api = Api(app)

# creates /auth for logging in
jwt = JWT(app, authenticate, get_identity)

# JWT token expires after 30 minutes (instead of default 10)
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5001, debug=True)

    # @app.before_first_request
    # def create_tables():
    #     db.create_all()
