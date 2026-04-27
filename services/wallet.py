from models.wallet import Wallet,WalletTransaction
from models.patient import Patient
from models.user import User
from services.daraja import call_daraja_api
from models.pays import Pay
from uuid import uuid4
def format_phone(phone:str)->str:
    phone=phone.strip().replace("","")
    if phone.startswith("+"):
        phone=phone[1:]
    if phone.startswith("07"):
        phone="254" + phone[1:]
    elif phone.startswith("01"):
        phone="254" + phone[1:]
    elif phone.startswith("254"):
        pass
    else:
        raise ValueError("Invalid phone number format")
    if len(phone) != 12 or not phone.isdigit():
        raise ValueError("Invalid phone number")
    return phone
def get_wallet_by_patient(db,patient_id:str):
    return db.query(Wallet).filter(Wallet.patient_id==patient_id).first()
def get_wallet_transactions(db,patient_id:str):
    wallet=get_wallet_by_patient(db,patient_id)
    return db.query(WalletTransaction).filter(WalletTransaction.wallet_id==wallet.wallet_id).order_by(WalletTransaction.created_at.desc()).all()
def debit_wallet(db,patient_id:str,amount:float,reference:str):
    wallet=get_wallet_by_patient(db,patient_id)
    if not wallet:
        wallet=Wallet(patient_id=patient_id,balance=0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    if wallet.balance < amount:
        return False
    wallet.balance -= amount
    txn=WalletTransaction(transaction_id=str(uuid4()),wallet_id=wallet.wallet_id,amount=amount,transaction_type="DEBIT",reference=reference)
    db.add(txn)
    db.commit()
    return True
def credit_wallet(db,patient_id:str,amount:float,reference:str):
    wallet=get_wallet_by_patient(db,patient_id)
    wallet.balance += amount
    txn=WalletTransaction(transaction_id=str(uuid4()),wallet_id=wallet.wallet_id,amount=amount,transaction_type="CREDIT",reference=reference)
    db.add(txn)
    db.commit()
    return True
def initiate_stk_push(db,Phone_number:str,amount:float,reference:str,current_user:User):
    formatted_phone=format_phone(Phone_number)
    visit_id=None
    if reference and "_" in reference:
        visit_id=reference.split("_")[1]
    response=call_daraja_api(phone=formatted_phone,amount=amount,reference=reference)
    checkout_id=response.get("CheckoutRequestID")
    payment=Pay(phone_number=formatted_phone,amount=amount,checkout_request_id=checkout_id,reference=reference,status="PENDING",visit_id=visit_id,clinical_id=current_user.hospital_id)
    db.add(payment)
    db.commit()
    return response
    

    