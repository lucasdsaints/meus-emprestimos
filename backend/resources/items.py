from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.items import ItemModel

class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Item's name is required."
     )
    # parser.add_argument(
    #     'user_id',
    #     type=int,
    #     required=True,
    #     help='User id is required.'
    # )

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        data['user_id'] = get_jwt_identity()
        item = ItemModel.find_by_name_and_user_id(**data)
        if item:
            return {'message': f'This user already has a item called {data["name"]}.'}
        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {'message': 'The application could not save this item.'}, 500
        return item.describe(), 201

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        return {'items': [item.describe() for item in ItemModel.find_all(user_id=user_id)]}

class SingleItem(Resource):
    @jwt_required
    def delete(self, id):
        item = ItemModel.find_by_id(id)
        if item:
            if item.user_id == get_jwt_identity():
                try:
                    item.delete_from_db()
                except:
                    return {'message': 'This item cannot be deleted.'}, 403
                return {'message': 'Item deleted successfully.'}, 204
            return {'message': 'This user cannot delete this item.'}, 403
        return {'message': 'There is no item with the given id.'}