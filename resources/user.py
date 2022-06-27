from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    def post(self):
        # parse and validate request arguments
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username", type=str, required=True, help="Username must be provided"
        )
        parser.add_argument(
            "password", type=str, required=True, help="Password must be provided"
        )
        data = parser.parse_args()

        # save (unique) user to database
        if UserModel.find_by_username(data["username"]):
            return {"message": f"A user named {data['username']} already exists!"}, 400

        user = UserModel(data["username"], data["password"])
        user.save_to_db()

        return {"message": f"User {data['username']} created sucessfully"}, 201
