import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

class Item(Resource):
    def __init__(self, _id, name):
        self.id = _id
        self.name = name

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="The item's name cannot be left blank.")

    @jwt_required()
    def post(self):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()

        data = self.parser.parse_args()     
        if self.get_by_name(data['name'], current_identity.id):
            connection.close()
            return {'message':  'Friend already registered'}, 400

        query = f'INSERT INTO items VALUES (NULL, ?, ?)'
        cursor.execute(query, (data['name'], current_identity.id))
        connection.commit()
        connection.close()

        return {'message': 'Item registered successfully.'}

    @jwt_required()
    def delete(self):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()

        data = self.parser.parse_args()
        if self.get_by_name(data['name'], current_identity.id) is None:
            connection.close()
            return {'message':  'Item not found'}, 404

        query = f'DELETE FROM items WHERE name = ? AND user = ?'
        cursor.execute(query, (data['name'], current_identity.id))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted successfully.'}

    @classmethod
    def get_by_name(cls, name, user_id):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()
        query = f'SELECT id, name FROM items WHERE name = "{name}" AND user = {user_id}'
        row = cursor.execute(query).fetchone()
        connection.close()
        if row:
            return cls(*row)

    @classmethod
    def get_by_id(cls, _id, user_id):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()
        query = f'SELECT id, name FROM items WHERE id = {_id} AND user = {user_id}'
        row = cursor.execute(query).fetchone()
        connection.close()
        if row:
            return cls(*row)

class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()

        query = f'SELECT id, name FROM items WHERE user = {current_identity.id}'
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'id': row[0], 'name': row[1]})
        connection.close()
        return {'items': items}, 200