from app import db
from flask import url_for

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    friends = db.relationship('FriendModel', backref='user', lazy='dynamic')
    items = db.relationship('ItemModel', backref='user', lazy='dynamic')
    loans = db.relationship('LoanModel', backref='user', lazy='dynamic')

    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name

    def describe(self, complete=True):
        response = {
            'id': self.id, 
            'username': self.username, 
            'name': self.name
        }
        if complete:
            response['items'] = [item.describe() for item in self.items]
            response['friends'] = [friend.describe() for friend in self.friends]
        else:
            response['items'] = url_for('items', _external=True)
            response['friends'] = url_for('friends', _external=True)
        
        return response

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
