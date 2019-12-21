from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.item_db import ItemModel


class Item(Resource):

    @jwt_required
    def get(self, name):
        current_user = get_jwt_identity()
        if not current_user:
            return {"message": "authentication error."}, 401

        try:
            result = ItemModel.find_item(name)
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500

        if result:
            return result.toDict(), 200
        return {"message": "item does not exist"}, 404


    @jwt_required
    def post(self, name):
        current_user = get_jwt_identity()
        if not current_user:
            return {"message": "authentication error."}, 401

        # This is one way to process the payload.
        # Notice that it's different from the PUT method.
        if not request.is_json:
            return {"message": "could not process json data"}, 400
        price = request.json.get("price", None)
        if not price:
            return {"message": "missing price parameter"}, 400
        store_id = request.json.get("store_id", None)
        if not store_id:
            return {"message": "missing store_id"}, 400

        try:
            if ItemModel.find_item(name):
                return {"message": "item already exists"}
            result = ItemModel(name, price, store_id).save_to_db()
            if result:
                return result.toDict(), 201
            return {"message": "Uh oh! Wrong timeline!"}, 500
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500


    @jwt_required
    def delete(self, name):
        current_user = get_jwt_identity()
        if not current_user:
            return {"message": "authentication error."}, 401

        try:
            item_to_delete = ItemModel.find_item(name)
            if item_to_delete:
                item_to_delete.delete_from_db()
                return item_to_delete.toDict(), 200
            return {"message": "item does not exist"}, 404
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500


    @jwt_required
    def put(self, name):
        current_user = get_jwt_identity()
        if not current_user:
            return {"message": "authentication error."}, 401

        # This is one way to process the payload.
        # Notice that it's different from the POST method.
        # Note: reqparse discards all other arguments not explicitly added by add_argument
        #       even if they are provided in the original payload
        parser = reqparse.RequestParser()
        parser.add_argument("price",
                            type=float,
                            required=True,
                            help="missing or invalid parameter price (float)")
        parser.add_argument("store_id",
                            type=int,
                            required=True,
                            help="missing or invalid parameter store_id (int)")

        data = parser.parse_args()
        price = data["price"]
        store_id = data["store_id"]

        try:
            result = ItemModel(name, price, store_id).save_to_db()
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500
        return result.toDict(), 200


class ItemList(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {"message": "authentication error."}, 401

        try:
            result = ItemModel.all_items()
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500
        return result, 200
