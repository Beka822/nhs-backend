from models.bill import Bill
from models.payment import Payment
from sqlalchemy.orm import Session
from models.user import User
from schemas.payment import PaymentCreate
from datetime import datetime
from models.audit_log import AuditLog
def create_payment(db:Session,data:PaymentCreate,bill_id:str,current_user:User):
    bill=db.query(Bill).filter(Bill.hospital_id==current_user.hospital_id,Bill.bill_id==bill_id).first()
    if not bill:
        raise ValueError("Bill not found")
    if data.amount<=0:
        raise ValueError("Payment must be positive")
    current_balance=bill.total_amount-bill.amount_paid
    if data.amount > current_balance:
        raise ValueError(f"You are supposed to pay {current_balance}")
    if data.amount<current_balance:
        raise ValueError(f"You are supposed to pay {current_balance}")
    payment=Payment(bill_id=bill.bill_id,remaining=current_balance-data.amount,amount=data.amount,payment_method=data.payment_method,reference_number=data.reference_number,received_by=current_user.user_id)
    db.add(payment)
    bill.amount_paid+=data.amount
    if bill.amount_paid>=bill.total_amount:
        bill.paid_at=datetime.utcnow()
    db.flush()
    if data.amount==current_balance:
        bill.paid_at=datetime.utcnow()
    db.add(AuditLog(action="CREATE_PAYMENT",entity="Payment",entity_id=payment.payment_id))
    db.commit()
    
    db.refresh(payment)
    return payment
def get_payments(db:Session,bill_id:str,current_user:User):
    bill=db.query(Bill).filter(Bill.bill_id==bill_id,Bill.hospital_id==current_user.hospital_id).first()
    if not bill:
        raise ValueError("Bill not found")
    payments=db.query(Payment).filter(Payment.bill_id==bill_id).order_by(Payment.received_at.desc()).all()
    return payments