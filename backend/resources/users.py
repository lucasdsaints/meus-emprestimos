from flask_restful import Resource, reqparse
from models.users import UserModel

class Users(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='Username is required.'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Password is required.'
    )
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='Name is required.'
    )

    def post(self):
        data = self.parser.parse_args()
        
        if UserModel.find_by_name(data['username']):
            return {'message': 'This user already exists.'}, 400

        user = UserModel(**data)
        
        try:
            user.save_to_db()
        except:
            return {'message': 'The application could not save this user.'}, 500
        return user.describe(), 201

    def get(self):
        return {'users': [user.describe() for user in UserModel.find_all()]}, 200