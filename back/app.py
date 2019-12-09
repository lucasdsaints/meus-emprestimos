from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT

from user import UserRegister
from security import authenticate, identity
from friend import Friend, FriendList
from item import Item, ItemList
from loan import LoanList, Loan, LoanStatus

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very-secret-password'
api = Api(app)
jwt = JWT(app, authenticate, identity)


api.add_resource(UserRegister, '/register')
api.add_resource(FriendList, '/friends')
api.add_resource(Friend, '/friend')
api.add_resource(Item, '/item')
api.add_resource(ItemList, '/items')
api.add_resource(LoanList, '/loans')
api.add_resource(Loan, '/loan')
api.add_resource(LoanStatus, '/loan/<int:_id>/<string:returned>')

if __name__ == "__main__":
    app.run(port=5000, debug=True)  