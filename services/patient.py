from sqlalchemy.orm import Session
from sqlalchemy import func
from models.patient import Patient
from models.audit_log import AuditLog
def create_patient(db:Session,data,current_user):
    existing=db.query(Patient).filter(Patient.patient_id==data.patient_id).first()
    if existing:
        raise ValueError("Patient ID already exists")
    patient=Patient(patient_id=data.patient_id,patient_name=data.patient_name,date_of_birth=data.date_of_birth,gender=data.gender,phone=data.phone,created_by=current_user["sub"])
    db.add(patient)
    db.commit()
    db.refresh(patient)
    audit=AuditLog(action="CREATE_PATIENT",entity="Patient",entity_id=patient.patient_id)
    db.add(audit)
    db.commit()
    return patient
def get_patient_by_id(db:Session,patient_id:str,current_user):
    patient=db.query(Patient).filter(Patient.patient_id==patient_id).first()
    if not patient:
        return None
    audit=AuditLog(action="READ_PATIENT",entity="Patient",entity_id=patient.patient_id)
    db.add(audit)
    db.commit()
    return patient
def get_all_patients(db:Session,current_user:dict,page:int,page_size:int):
    query=db.query(Patient)
    total=db.query(func.count(Patient.id)).scalar()
    patients=(query.offset((page-1)*page_size).limit(page_size).all())
    audit=AuditLog(action="READ_ALL",entity="Patient",entity_id=current_user["sub"])
    db.add(audit)
    db.commit()
    return {"page":page,"page_size":page_size,"total":total,"total_pages":(total+page_size-1) // page_size,"items":patients}