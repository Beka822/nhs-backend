from datetime import datetime
from sqlalchemy.orm import Session
from models.bed import Bed
from models.user import User
from models.ward import Ward
from schemas.bed import BedCreateRequest,BedResponse
from models.audit_log import AuditLog
def create_bed(db:Session,bed_data:BedCreateRequest,current_user:User,ip_address:str):
    if current_user.role not in ["ADMIN","DOCTOR","NURSE"]:
        raise PermissionError("Not authorized")
    ward=db.query(Ward).filter(Ward.hospital_id==current_user.hospital_id,Ward.ward_id==bed_data.ward_id).first()
    if not ward:
        raise ValueError("Ward not found")
    existing_bed=db.query(Bed).filter(Bed.hospital_id==current_user.hospital_id,Bed.ward_id==bed_data.ward_id,Bed.code==bed_data.code).first()
    if existing_bed:
        raise ValueError("Bed code already exists")
    bed=Bed(ward_id=bed_data.ward_id,code=bed_data.code,is_icu=bed_data.is_icu,status="AVAILABLE",created_at=datetime.utcnow(),hospital_id=current_user.hospital_id)
    db.add(bed)
    audit=AuditLog(action="CREATE_BED",entity="Bed",entity_id=bed.code)
    db.add(audit)
    db.commit()
    db.refresh(bed)
    return bed
def get_beds(db:Session,current_user:User,ward_id:str|None=None):
    query=db.query(Bed).filter(Bed.hospital_id==current_user.hospital_id)
    if ward_id:
        query=query.filter(Bed.hospital_id==current_user.hospital_id,Bed.ward_id==ward_id)
    return query.all()
def update_bed(db:Session,bed_id:str,update_data:dict,current_user:User,ip_address:str):
    bed=db.query(Bed).filter(Bed.hospital_id==current_user.hospital_id,Bed.bed_id==bed_id).first()
    if not bed:
        raise ValueError("Bed not found")
    for field in ["code","is_icu","status"]:
        if field in update_data:
            setattr(bed,field,update_data[field])
    audit=AuditLog(action="UPDATE_BED",entity="Bed",entity_id=bed.code)
    db.add(audit)
    db.commit()
    db.refresh(bed)
    return bed
def delete_bed(db:Session,bed_id:str,current_user:User,ip_address:str):
    bed=db.query(Bed).filter(Bed.hospital_id==current_user.hospital_id,Bed.bed_id==bed_id).first()
    if not bed:
        raise ValueError("Bed not found")
    if bed.status != "AVAILABLE":
        raise ValueError("Cannot delete bed that is currently occupied")
    audit=AuditLog(action="DELETE_BED",entity="Bed",entity_id=bed.code)
    db.add(audit)
    db.delete(bed)
    db.commit()
    return {"message":f"Bed {bed.code} deleted successfully"}

