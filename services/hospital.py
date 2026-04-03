from sqlalchemy.orm import Session
from models.hospital import Hospital
from models.user import User
from models.audit_log import AuditLog
def register_hospital(db:Session,hospital_id:str,hospital_name:str,county:str,current_user:User):
    if current_user.role !="SUPER_ADMIN":
        raise PermissionError("You are not authorized to register a hospital")

    existing=db.query(Hospital).filter(Hospital.hospital_id==hospital_id).first()
    if existing:
        raise ValueError("Hospital ID already exists")
    hospital=Hospital(hospital_id=hospital_id,hospital_name=hospital_name,county=county)
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    audit=AuditLog(action="CREATE HOSPITAL",entity="Hospital",entity_id=hospital.hospital_id)
    db.add(audit)
    db.commit()
    return hospital
def get_hospital_by_id(db:Session,hospital_id:str):
    hospital=db.query(Hospital).filter(Hospital.hospital_id==hospital_id).first()
    if not hospital:
        return None
    return hospital
def get_all_hospitals(db:Session):
    return db.query(Hospital).all()
