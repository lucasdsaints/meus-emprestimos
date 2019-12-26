from flask_restful import Resource, reqparse

from models.friends import FriendModel

class Friends(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Friend's name is required."
    )
    parser.add_argument(
        'user_id',
        type=int,
        required=True,
        help='User id is required.'
    )

    def post(self):
        data = self.parser.parse_args()
        friend = FriendModel.find_by_name_and_user_id(**data)
        if friend:
            return {'message': f'This user already has a friend called {data["name"]}.'}
        friend = FriendModel(**data)

        try:
            friend.save_to_db()
        except:
            return {'message': 'The application could not save this friend.'}, 500
        return friend.describe(), 201

    def get(self):
        return {'friends': [friend.describe() for friend in FriendModel.find_all()]}

class SingleFriend(Resource):
    def delete(self, id):
        friend = FriendModel.find_by_id(id)
        if friend:
            friend.delete_from_db()
        return {'message': 'Friend deleted successfully.'}