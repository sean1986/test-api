from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        if store := StoreModel.find_by_name(name):
            return store.json()

        return {"message": f"Store '{name}' not found!"}, 404

    def post(self, name):
        if store := StoreModel.find_by_name(name):
            return {"message": f"Store '{name}' already exists!"}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "Error creating store!"}, 500

        return store.json(), 201

    def delete(self, name):
        if store := StoreModel.find_by_name(name):
            store.delete_from_db()
            return store.json()

        return {"message": f"No store '{name}' to delete!"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
