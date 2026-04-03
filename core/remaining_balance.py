from sqlalchemy import func
from sqlalchemy.orm import Session
from models.bill import Bill
from models.payment import Payment
def get_balance(db:Session,admission_id:str,bill_id:str):
    total_bills=(db.query(func.sum(Bill.amount_paid)).filter(Bill.admission_id==admission_id).scalar()) or 0
    total_payments=(db.query(func.sum(Payment.amount)).filter(Payment.bill_id==bill_id).scalar()) or 0
    remaining_balance=total_bills-total_payments
    return {"total_bills":total_bills,"total_payments":total_payments,"remaining_balance":remaining_balance}
