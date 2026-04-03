from models.admission import Admission
from datetime import datetime
from sqlalchemy.orm import Session
from schemas.admission import AdmissionCreate
from models.user import User
from models.bed import Bed
from models.patient import Patient
from models.audit_log import AuditLog
from core.exceptions import UnauthorizedAccess,ResourceNotFound
async def create_admission(data:AdmissionCreate,db:Session,visit_id:str,current_user:User):
    if current_user.role not in ["ADMIN","DOCTOR","NURSE"]:
        raise PermissionError("Not authorized to admit a patient")
    patient=db.query(Patient).filter(Patient.patient_id==data.patient_id).first()
    if not patient:
        raise ResourceNotFound("Patient")
    existing=(db.query(Admission).filter(Admission.hospital_id==current_user.hospital_id,Admission.patient_id==data.patient_id,Admission.discharge_at.is_(None)).first())
    if existing:
        raise ValueError("Patient already has an active admission")
    bed=db.query(Bed).filter(Bed.hospital_id==current_user.hospital_id,Bed.bed_id==data.bed_id,Bed.status=="AVAILABLE").first()
    if not bed:
        raise ResourceNotFound("Bed")
    if bed.status != "AVAILABLE":
        raise ValueError(f"Bed {bed.bed_id} is not available. Current status: {bed.status}")
    admission=Admission(patient_id=data.patient_id,visit_id=visit_id,bed_id=data.bed_id,hospital_id=current_user.hospital_id,created_by=current_user.user_id)
    db.add(admission)
    db.flush()
    bed.status="OCCUPIED"
    db.add(AuditLog(action="CREATE_ADMISSION",entity="Admission",entity_id=admission.admission_id))
    db.commit()
    db.refresh(admission)
    
    return admission
async def discharge_patient(db:Session,admission_id:str,current_user:User):
    if current_user.role not in ["ADMIN","DOCTOR"]:
        raise PermissionError("Not authorized to discharge a patient")
    admission=db.query(Admission).filter(Admission.admission_id==admission_id,Admission.hospital_id==current_user.hospital_id).first()
    if not admission:
        raise ResourceNotFound("Admission")
    if admission.discharge_at is not None:
        raise ValueError("Patient already discharged")
    admission.discharge_at=datetime.utcnow()
    bed=db.query(Bed).filter(Bed.hospital_id==current_user.hospital_id,Bed.bed_id==admission.bed_id).first()
    if bed:
        bed.status="AVAILABLE"
    db.add(AuditLog(action="DISCHARGE",entity="Admission",entity_id=admission.admission_id))
    db.commit()
    db.refresh(admission)
    
    return admission
def get_active_admissions(db:Session,hospital_id:str,visit_id:str):
    return (db.query(Admission).filter(Admission.hospital_id==hospital_id,Admission.discharge_at.is_(None),visit_id==visit_id).all())
    