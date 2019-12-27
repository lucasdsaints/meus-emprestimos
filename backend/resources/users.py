from flask_restful import Resource, reqparse
from models.users import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_optional, get_jwt_identity

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
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'This user already exists.'}, 400

        user = UserModel(**data)
        
        try:
            user.save_to_db()
        except:
            return {'message': 'The application could not save this user.'}, 500
        return user.describe(), 201

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        if user_id:
            user = UserModel.find_by_id(user_id)
            return user.describe(), 200
        return {'users': [user.describe() for user in UserModel.find_all()]}, 200


class UserLogin(Resource):
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
    
    def post(self):
        data = self.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401