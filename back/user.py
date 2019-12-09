import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, name, password):
        self.id = _id
        self.name = name
        self.password = password

    @classmethod
    def get_by_id(cls, _id):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM users WHERE id = ?'
        row = cursor.execute(query, (_id,)).fetchone()
        connection.close()
        if row:
            return cls(*row)

    @classmethod
    def get_by_name(cls, name):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()
        query = 'SELECT id, name, password FROM users WHERE name = ?'
        row = cursor.execute(query, (name,)).fetchone()
        connection.close()
        if row:
            return cls(*row)


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='Password cannot be left blank')

    def post(self):
        data = self.parser.parse_args()
        if User.get_by_name(data['username']):
            return {'message': 'This user already exists.'}, 400
        
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users VALUES(NULL, ?, ?)', (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {'message': 'user created successfully'}, 201