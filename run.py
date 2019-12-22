import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from apis.item_apis import Item, ItemList
from apis.user_apis import Users, Login
from apis.store_apis import Store, StoreList
from database.user_db import UserModel
from sqlalchemy_db import db


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "johnsmith"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
jwt = JWTManager(app)
api = Api(app)
db.init_app(app)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Users, "/user")
api.add_resource(Login, "/login")


@app.before_first_request
def first_run_init():
    print("First run initialization...")
    db.create_all()
    create_admin()


def create_admin():
    if not UserModel.find_by_username("admin"):
        print("admin created")
        UserModel("admin", "admin123", True).save_to_db()

