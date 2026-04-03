from models.audit_log import AuditLog
from models.bill import Bill
from datetime import datetime
from models.payment import Payment
from models.patient import Patient
from models.admission import Admission
from models.visit import Visit
from models.user import User
def build_bill_response(db,bill):
    visit=db.query(Visit).filter(Visit.visit_id==bill.visit_id).first()
    patient_name=None
    if visit:
        patient=db.query(Patient).filter(Patient.patient_id==visit.patient_id).first()
        if patient:
            patient_name=patient.patient_name
    return{
        "bill_id":bill.bill_id,
        "visit_id":bill.visit_id,
        "admission_id":bill.admission_id,
        "patient_id":bill.patient_id,
        "patient_name":patient_name,
        "total_amount":bill.total_amount,
        "amount_paid":bill.amount_paid,
        "created_at":bill.created_at,
        "paid_at":bill.paid_at
    }
def create_bill(db,visit_id,data,current_user:User):
    hospital_id=current_user.hospital_id
    visit=db.query(Visit).filter(Visit.visit_id==visit_id,Visit.hospital_id==current_user.hospital_id).first()
    if not visit:
        raise ValueError("Visit not found")
    admission_id=data.admission_id
    if admission_id:
        admission=db.query(Admission).filter(Admission.admission_id==admission_id,Admission.hospital_id==current_user.hospital_id,Admission.discharge_at==None).first()
        if not admission:
            raise ValueError("Active admission not found")
    else:
        admission_id=None
    bill=Bill(hospital_id=hospital_id,visit_id=visit_id,admission_id=admission_id,patient_id=visit.patient_id,total_amount=0,amount_paid=0)
    db.add(bill)
    db.flush()
    audit=AuditLog(action="CREATE_BILL",entity="Bill",entity_id=bill.bill_id)
    db.add(audit)
    db.commit()
    db.refresh(bill)
    return build_bill_response(db,bill)
def get_all_bills(db,current_user:User,start_date=None,end_date=None):
    query=db.query(Bill).filter(Bill.hospital_id==current_user.hospital_id)
    if start_date:
        query=query.filter(Bill.created_at >= start_date)
    if end_date:
        query=query.filter(Bill.created_at <= end_date)
    bills=db.query(Bill).filter(Bill.hospital_id==current_user.hospital_id).order_by(Bill.created_at.desc()).all()
    results=[]
    for bill in bills:
        visit=db.query(Visit).filter(Visit.visit_id==bill.visit_id).first()
        patient_name=None
        if visit:
            patient=db.query(Patient).filter(Patient.patient_id==visit.patient_id).first()
            if patient:
                patient_name=patient.patient_name
        results.append({
            "bill_id":bill.bill_id,
            "admission_id":bill.admission_id,
            "visit_id":bill.visit_id,
            "patient_id":bill.patient_id,
            "patient_name":patient_name,
            "total_amount":bill.total_amount,
            "amount_paid":bill.amount_paid,
            "created_at":bill.created_at,
            "paid_at":bill.paid_at
        })
    return results
def get_bill(db,bill_id,current_user:User):
    hospital_id=current_user.hospital_id
    bill=db.query(Bill).filter(Bill.bill_id==bill_id,Bill.hospital_id==hospital_id).first()
    if not bill:
        raise ValueError("Bill not found")
    return build_bill_response(db,bill)

    




