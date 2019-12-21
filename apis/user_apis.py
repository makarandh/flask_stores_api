from flask import request
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from conf.security import authenticate
from database.user_db import UserModel


class Users(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        try:
            user = UserModel.find_by_username(current_user).toDict()
            if user:
                return user, 200
            return {"message": "user does not exist"}, 404
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500


    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        try:
            user = UserModel.find_by_username(current_user).toDict()
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500

        if not user["admin"]:
            return {"message": "you are not authorized to do that"}, 401

        parser = reqparse.RequestParser()
        parser.add_argument("username",
                            type=str,
                            required=True,
                            help="could not parse username")

        parser.add_argument("password",
                            type=str,
                            required=True,
                            help="could not parse password")

        parser.add_argument("admin", type=bool, required=False)
        data = parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return ({"message": "user already exists"}), 400

        try:
            status = UserModel(**data).save_to_db()
            if status:
                return status.toDict(), 201
            return {"message": "uh oh! Wrong timeline!"}, 500

        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500


class Login(Resource):
    def post(self):
        if not request.is_json:
            return {"message": "could not process json data"}, 400

        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username:
            return {"message": "missing username parameter"}, 400
        if not password:
            return {"message": "missing password parameter"}, 400

        try:
            user = authenticate(username, password)
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500

        if user:
            access_token = create_access_token(identity=username)
            return {"access_token": access_token}, 200
        return {"message": "invalid username and/or password."}, 400

