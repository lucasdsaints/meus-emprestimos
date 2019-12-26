from flask_restful import Resource, reqparse

from models.loans import LoanModel

class Loans(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'id_user',
        type=int,
        required=True,
        help="User's id is required."
    )
    parser.add_argument(
        'id_friend',
        type=int,
        required=True,
        help="Friend's id is required."
    )
    parser.add_argument(
        'id_item',
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
        pass

    def get(self):
        pass

class SingleLoan(Resource):
    def put(self, _id):
        pass