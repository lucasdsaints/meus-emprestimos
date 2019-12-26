from flask import Flask
from flask_restful import Api

from common.db import db
from common.config import Config
from resources.users import Users
from resources.friends import Friends, SingleFriend
from resources.items import Items, SingleItem
from resources.loans import Loans, SingleLoan

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_db():
    db.create_all()

api.add_resource(Users, '/users')
api.add_resource(Friends, '/friends')
api.add_resource(SingleFriend, '/friends/<int:id>')
api.add_resource(Items, '/items')
api.add_resource(SingleItem, '/items/<int:id>')
api.add_resource(Loans, '/loans')
api.add_resource(SingleLoan, '/loans/<int:id>')