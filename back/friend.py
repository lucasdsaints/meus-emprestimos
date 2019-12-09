import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

class Friend(Resource):
    def __init__(self, _id, name):
        self.id = _id
        self.name = name

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="The friend's name cannot be left blank.")

    @jwt_required()
    def post(self):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()

        data = self.parser.parse_args()     
        if self.get_by_name(data['name'], current_identity.id):
            connection.close()
            return {'message':  'Friend already registered'}, 400

        query = f'INSERT INTO friends VALUES (NULL, ?, ?)'
        cursor.execute(query, (data['name'], current_identity.id))
        connection.commit()
        connection.close()

        return {'message': 'Friend registered successfully.'}

    @jwt_required()
    def delete(self):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()

        data = self.parser.parse_args()
        if self.get_by_name(data['name'], current_identity.id) is None:
            connection.close()
            return {'message':  'Friend not found'}, 404

        query = f'DELETE FROM friends WHERE name = ? AND user = ?'
        cursor.execute(query, (data['name'], current_identity.id))
        connection.commit()
        connection.close()
        return {'message': 'Friend deleted successfully.'}

    @classmethod
    def get_by_name(cls, name, user_id):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()
        query = f'SELECT id, name FROM friends WHERE name = {name} AND user = {user_id}'
        row = cursor.execute(query).fetchone()
        connection.close()
        if row:
            return cls(*row)

    @classmethod
    def get_by_id(cls, _id, user_id):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()
        query = f'SELECT id, name FROM friends WHERE id = {_id} AND user = {user_id}'
        row = cursor.execute(query).fetchone()
        connection.close()
        if row:
            return cls(*row)

class FriendList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()

        query = f'SELECT id, name FROM friends WHERE user = {current_identity.id}'
        result = cursor.execute(query)
        friends = []
        for row in result:
            friends.append({'id': row[0], 'name': row[1]})
        connection.close()
        return {'friends': friends}, 200