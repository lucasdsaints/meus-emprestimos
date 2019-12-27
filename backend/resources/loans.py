from flask_restful import Resource, reqparse

from models.loans import LoanModel
from models.friends import FriendModel
from models.items import ItemModel

class Loans(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'user_id',
        type=int,
        required=True,
        help="User's id is required."
    )
    parser.add_argument(
        'friend_id',
        type=int,
        required=True,
        help="Friend's id is required."
    )
    parser.add_argument(
        'item_id',
        type=int,
        required=True,
        help="Item's id is required."
    )
    parser.add_argument(
        'loan_type',
        type=str,
        required=True,
        help="Loan type is required."
    )
    parser.add_argument(
        'description',
        type=str,
        required=False
    )


    def post(self):
        data = self.parser.parse_args()
        
        if FriendModel.find_by_id(data['friend_id']) is None:
            return {'message': f'There is no friend with id {data["friend_id"]}'}
        
        if ItemModel.find_by_id(data['item_id']) is None:
            return {'message': f'There is no item with id {data["item_id"]}'}
       
        data['loan_type'] = 0 if data['loan_type'] == 'friend_to_user' else 1
        loan = LoanModel(**data)
        
        try:
            loan.save_to_db()
        except:
            return {'message': 'The application could not save this loan.'}, 500

        return loan.describe()

    def get(self):
        return {'loans': [loan.describe() for loan in LoanModel.find_all()]}

class SingleLoan(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'status',
        type=str,
        required=True,
        help='the status should be informed.')
    def put(self, id):
        data = self.parser.parse_args()
        loan = LoanModel.find_by_id(id)
        if loan is None:
            return {'message': f'There is no loan with id {id}.'}
        loan.status = 1 if data['status'] == 'active' else 0
        print(loan.status)
        loan.save_to_db()
        return loan.describe()