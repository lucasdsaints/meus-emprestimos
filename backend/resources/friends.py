from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.friends import FriendModel

class Friends(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Friend's name is required."
    )

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        data['user_id'] = get_jwt_identity()
        friend = FriendModel.find_by_name_and_user_id(**data)
        if friend:
            return {'message': f'This user already has a friend called {data["name"]}.'}
        friend = FriendModel(**data)

        try:
            friend.save_to_db()
        except:
            return {'message': 'The application could not save this friend.'}, 500
        return friend.describe(), 201
    
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        return {'friends': [friend.describe() for friend in FriendModel.find_all(user_id=user_id)]}

class SingleFriend(Resource):
    @jwt_required
    def delete(self, id):
        friend = FriendModel.find_by_id(id)
        if friend:
            if friend.user_id == get_jwt_identity():
                try:
                    friend.delete_from_db()
                except:
                    return {'message': 'This friend cannot be deleted.'}, 403
                return {'message': 'Friend deleted successfully.'}, 204 # No Content
            return {'message': 'This user cannot delete this friend.'}, 403 # Forbidden
        return {'message': 'There is no frind with the given id.'}, 400 # Bab Request