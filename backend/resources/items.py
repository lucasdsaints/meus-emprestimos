from flask_restful import Resource, reqparse

from models.items import ItemModel

class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Item's name is required."
    )
    parser.add_argument(
        'user_id',
        type=int,
        required=True,
        help='User id is required.'
    )

    def post(self):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name_and_user_id(**data)
        if item:
            return {'message': f'This user already has a item called {data["name"]}.'}
        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {'message': 'The application could not save this item.'}, 500
        return item.describe(), 201

    def get(self):
        return {'items': [item.describe() for item in ItemModel.find_all()]}

class SingleItem(Resource):
    def delete(self, id):
        item = ItemModel.find_by_id(id)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted successfully.'}