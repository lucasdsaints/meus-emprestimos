from app import db

class LoanModel(db.Model):
    __tablename__ = 'loan'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    loan_type = db.Column(db.Integer, default=0, nullable=False)
    description = db.Column(db.String(30), nullable=True)
    status = db.Column(db.Integer, default=1, nullable=False)


    def __init__(self, user_id, friend_id, item_id, loan_type, description, status=1):
        self.user_id = user_id
        self.friend_id = friend_id
        self.item_id = item_id
        self.loan_type = loan_type
        self.description = description
        self.status = status
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def describe(self):
        return {
            'id': self.id, 
            'user_id': self.user_id,
            'user_name': self.user.name,
            'friend_id': self.friend_id,
            'friend_name': self.friend.name,
            'item_id': self.item_id,
            'item_name': self.item.name,
            'loan_type': 'friend_to_user' if self.loan_type == 0 else 'user_to_friend',
            'description': self.description,
            'status': 'active' if self.status == 1 else 'inactive'
        }

    @classmethod
    def find_all(cls, user_id=None):
        if user_id:
            return cls.query.filter_by(user_id=user_id)
        return cls.query.all()

    @classmethod
    def find_by_name_and_user_id(cls, name, user_id):
        return cls.query.filter_by(name=name, user_id=user_id).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()