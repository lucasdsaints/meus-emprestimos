from app import db

class ItemModel(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    loans = db.relationship('LoanModel', backref='item', lazy='dynamic')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def describe(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'item_of': self.user.name,
            'user_id': self.user_id
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