from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Float

db = SQLAlchemy()

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    oldbalanceOrg = db.Column(db.Float, nullable=False)
    newbalanceOrg = db.Column(db.Float, nullable=False)
    oldbalanceDest = db.Column(db.Float, nullable=False)
    newbalanceDest = db.Column(db.Float, nullable=False)
    type_CASH_IN = db.Column(db.Integer, nullable=False)
    type_CASH_OUT = db.Column(db.Integer, nullable=False)
    type_DEBIT = db.Column(db.Integer, nullable=False)
    type_PAYMENT = db.Column(db.Integer, nullable=False)
    type_TRANSFER = db.Column(db.Integer, nullable=False)
    isFraud = db.Column(db.Integer, nullable=False)

    def __init__(self, step, amount, oldbalanceOrg, newbalanceOrg, oldbalanceDest, newbalanceDest, type_CASH_IN, type_CASH_OUT, type_DEBIT, type_PAYMENT, type_TRANSFER, isFraud):
        self.step = step
        self.amount = amount
        self.oldbalanceOrg = oldbalanceOrg
        self.newbalanceOrg = newbalanceOrg
        self.oldbalanceDest = oldbalanceDest
        self.newbalanceDest = newbalanceDest
        self.type_CASH_IN = type_CASH_IN
        self.type_CASH_OUT = type_CASH_OUT
        self.type_DEBIT = type_DEBIT
        self.type_PAYMENT = type_PAYMENT
        self.type_TRANSFER = type_TRANSFER
        self.isFraud = isFraud
