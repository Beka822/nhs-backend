from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from core.db import get_db
from models.user import User
from models.services import Service
from core.dependencies import get_user_object
from schemas.services import ServiceCreate
router=APIRouter(prefix="/service",tags=["Services"])
@router.post("/")
def create_service(data:ServiceCreate,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    existing=db.query(Service).filter(Service.hospital_id==current_user.hospital_id,Service.name.ilike(data.name.strip())).first()
    if existing:
        raise ValueError("Service already exists")
    service=Service(hospital_id=current_user.hospital_id,name=data.name.strip(),price=data.price)
    db.add(service)
    db.commit()
    db.refresh(service)
    return {
        "service_id":service.service_id,
        "name":service.name,
        "price":service.price
    }
@router.get("/")
def get_services(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    services=db.query(Service).filter(Service.hospital_id==current_user.hospital_id,Service.is_active==True).all()
    return [
        {
            "service_id":s.service_id,
            "name":s.name,
            "price":s.price
        }
        for s in services
    ]