import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from item import Item
from friend import Friend

class LoanList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()
        query = '''
            SELECT l.id AS loan_id,
                   l.loan_type,
                   l.returned,
                   u.name AS user,
                   f.name AS friend,
                   i.name AS item
              FROM loans AS l 
             INNER JOIN users AS u ON l.user = u.id
             INNER JOIN friends AS f ON l.friend = f.id
             INNER JOIN items AS i ON l.item = i.id
             WHERE 1 = 1
               AND u.id = ?;
        '''
        result = cursor.execute(query, (current_identity.id,))
        loans = []
        for row in result:
            loans.append({
                'id': row[0],
                'loan_type': row[1],
                'returned': row[2],
                'user': row[3],
                'friend': row[4],
                'item': row[5]
            })
        connection.close()
        return {'loans': loans}, 200

class Loan(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('friend_id', type=int, required=True, help="The friend's id must be informed.")
        parser.add_argument('item_id', type=int, required=True, help="The item's id must be informed.")
        parser.add_argument('loan_type', type=int, required=True, help="The loan type must be informed.")

        data = parser.parse_args()
        user = current_identity
        print(data['friend_id'], data['item_id'], user.id)
        friend = Friend.get_by_id(data['friend_id'], user.id)
        item = Item.get_by_id(data['item_id'], user.id)

        if friend is None or item is None:
            return {'message': 'The friend or item informed do not exists for this user.'}, 400

        query = 'INSERT INTO loans VALUES(NULL, ?, ?, ?, ?, ?)'
        values = user.id, friend.id, item.id, data['loan_type'], 'NO'
        connection = sqlite3.connect('storage.db')
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        connection.close()
        return {'message': 'Loan registered successfully'}, 201

class LoanStatus(Resource):
    @jwt_required()
    def put(self, _id, returned):
        connetion = sqlite3.connect('storage.db')
        cursor =connetion.cursor()
        
        query = f'SELECT * FROM loans WHERE id = {_id}'
        if cursor.execute(query).fetchone() is None:
            return {'message': 'Loan not found.'}, 404
        
        query = f'UPDATE loans SET returned = "{returned}" WHERE id = {_id}'
        connetion.execute(query)

        connetion.commit()
        connetion.close()
        return {'message': 'Loan updated successfully.'}, 200



