from sqlalchemy.orm import Session
from models.ward import Ward
from models.audit_log import AuditLog
from fastapi import Depends
from core.dependencies import get_current_user
from models.user import User
from schemas.ward import WardCreate,WardUpdate
def create_ward(db:Session,data:WardCreate,current_user:User):

    existing=db.query(Ward).filter(Ward.code==data.code,Ward.hospital_id==current_user.hospital_id).first()
    if existing:
        raise ValueError("Ward code already exists")
    ward=Ward(name=data.name,code=data.code,hospital_id=current_user.hospital_id,ward_type=data.ward_type,capacity=data.capacity,floor=data.floor)
    if ward.hospital_id != current_user.hospital_id:
        raise ValueError("Not allowed")

    db.add(ward)
    
    db.add(AuditLog(action="CREATE_WARD",entity="Ward",entity_id=data.code))
    db.commit()
    db.refresh(ward)
    return ward
def get_wards(db:Session,hospital_id:str,current_user:User):
    ward=db.query(Ward).filter(Ward.hospital_id==current_user.hospital_id).first()
    if not ward:
        raise ValueError("Ward not found")
    if ward.hospital_id !=current_user.hospital_id:
        raise ValueError("Not allowed")
    return db.query(Ward).filter(Ward.hospital_id==hospital_id).all()
def update_ward(db:Session,ward_id:str,data:WardUpdate,current_user:User,ip_address:str):
    ward=db.query(Ward).filter(Ward.ward_id==ward_id,Ward.hospital_id==current_user.hospital_id).first()
    if not ward:
        raise ValueError("Ward not found")
    for field,value in data.dict(exclude_unset=True).items():
        setattr(ward,field,value)
    db.add(AuditLog(action="UPDATE_WARD",entity="Ward",entity_id=ward.code))
    db.commit()
    db.refresh(ward)
    return ward
def delete_ward(db:Session,ward_id:str,current_user:User,ip_address:str):
    ward=db.query(Ward).filter(Ward.ward_id==ward_id,Ward.hospital_id==current_user.hospital_id).first()
    if not ward:
        raise ValueError("Ward not found")
    ward.is_active=False
    db.add(AuditLog(action="DIACTIVATE_WARD",entity="Ward",entity_id=ward.code))
    db.commit()
    return {"message": "Ward deactivated"}
