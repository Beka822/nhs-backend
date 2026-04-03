
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.visit import Visit
from models.hospital import Hospital
from services.wallet import debit_wallet,initiate_stk_push
from models.patient import Patient
from models.user import User
from models.audit_log import AuditLog
VISIT_FEE=20
def create_visit(db:Session,data,current_user:User):
    try:
        patient=db.query(Patient).filter(Patient.patient_id==data.patient_id).first()
        if not patient:
            raise ValueError("Patient not found")
        visit=Visit(patient_id=patient.patient_id,symptoms=data.symptoms,diagnosis=data.diagnosis,treatment=data.treatment,notes=data.notes,hospital_id=current_user.hospital_id,created_by=current_user.user_id,payment_status="PENDING")
        db.add(visit)
        db.flush()
        reference=f"visit_{visit.visit_id}"
        success=debit_wallet(db=db,patient_id=patient.patient_id,amount=VISIT_FEE,reference=reference)
        try:
            stk_response=initiate_stk_push(Phone_number=patient.phone,amount=VISIT_FEE)
        except Exception:
            stk_response={"message": "STK failed"}
        audit=AuditLog(action="CREATE_VISIT_PENDING",entity="Visit",entity_id=visit.visit_id)
        db.add(audit)
        db.commit()
        db.refresh(visit)
        return {
            "status": "PENDING",
            "visit": visit,
            "stk": stk_response
        }
    except Exception as e:
        db.rollback
        raise e
def get_visit_by_id(db:Session,patient_id:str,visit_id:str):
    return db.query(Visit).filter(Visit.patient_id==patient_id,Visit.visit_id==visit_id).first()
def get_all_visits_for_patient(db:Session,patient_id:str):
    return db.query(Visit).filter(Visit.patient_id==patient_id).all()
