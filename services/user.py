from sqlalchemy.orm import Session
from fastapi import Depends
from core.db import get_db
from core.dependencies import get_user_object

from models.user import User,UserRoles
from models.hospital import Hospital
from models.audit_log import AuditLog
from core.security import hash_password
def create_user(db:Session,user_id:str,full_name:str,hospital_id:str,role:UserRoles,password:str):
    existing=db.query(User).filter(User.hospital_id==hospital_id,User.user_id==user_id).first()
    if existing:
        raise ValueError("User ID already exists")
    if role != "SUPER_ADMIN" and not hospital_id:
        raise ValueError("Hospital id is required for this role")
    if role=="SUPER_ADMIN" and hospital_id:
        raise ValueError("SUPER_ADMIN cannot belong to a hospital")
    user=User(user_id=user_id,full_name=full_name,hospital_id=hospital_id,role=role,hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    audit=AuditLog(action="CREATE_USER",entity="User",entity_id=user.user_id)
    db.add(audit)
    db.commit()
    return user
def get_user_by_id(db:Session,user_id:str,current_user:User):
    user=db.query(User).filter(User.hospital_id==Hospital.hospital_id,User.user_id==user_id).first()
    return user
def get_all_users(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    if current_user.role not in ["SUPER_ADMIN","ADMIN"]:
        raise PermissionError("Not authorized")
    return db.query(User).filter(User.hospital_id==current_user.hospital_id).all()
