#!/usr/bin/env python

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

    def _check_request_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "price",
            type=float,
            required=True,
            help="Item's price must be provided",
        )
        parser.add_argument(
            "store_id",
            type=int,
            required=True,
            help="Each item must have a store ID.",
        )
        return parser.parse_args()

    @jwt_required()
    def get(self, name):
        if item := ItemModel.find_by_name(name):
            return item.json()

        return {"message": f"Item '{name}' not found!"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"error": f"Item {name} already exists!"}, 400

        data = self._check_request_args()
        item = ItemModel(name, data["price"], data["store_id"])

        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        if item := ItemModel.find_by_name(name):
            item.delete_from_db()
            return item.json(), 201

        return {"error": f"Item not found: {name}"}, 404

    @jwt_required()
    def put(self, name):
        data = self._check_request_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
            status_code = 201
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
            status_code = 200

        item.save_to_db()

        return item.json(), status_code


class ItemList(Resource):

    @jwt_required()
    def get(self):
        return {"items": [item.json() for item in ItemModel.get_all_items()]}
