from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from database.store_db import StoreModel


class Store(Resource):

    @jwt_required
    def get(self, name):
        current_user = get_jwt_identity()
        if not current_user:
            return {"message": "authentication error."}, 401

        try:
            store = StoreModel.find_by_name(name)
        except Exception as e:
            print("Error {}".format(e))
            return {"message": "internal server error"}, 500

        if store:
            return store.toDict(), 200
        return {"message": "store not found"}, 404


    @jwt_required
    def post(self, name):
        current_user = get_jwt_identity()
        if not current_user:
            return {"message": "authentication error."}, 401

        try:
            if StoreModel.find_by_name(name):
                return {"message": "store already exist"}, 400

            result = StoreModel(name).save_to_db()
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
            store_to_delete = StoreModel.find_by_name(name)
            if store_to_delete:
                store_to_delete.delete_from_db()
                return store_to_delete.toDict(), 200
            return {"message": "store does not exist"}, 404
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500


class StoreList(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if not current_user:
            return {"message": "authentication error."}, 401

        try:
            result = StoreModel.all_items()
        except Exception as e:
            print("Error: {}".format(e))
            return {"message": "internal server error"}, 500
        return result, 200



