from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from core.permissions import require_roles
from models.user import User
from core.dependencies import get_user_object
from core.db import get_db
from schemas.hospital import HospitalCreate,HospitalResponse
from services.hospital import (register_hospital,get_hospital_by_id,get_all_hospitals)
router=APIRouter(prefix="/hospitals",tags=["Hospitals"])
@router.post("/",response_model=HospitalResponse)
def create_hospital(hospital_data:HospitalCreate,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),s_:dict=Depends(require_roles("SUPER_ADMIN"))):
    try:
        return register_hospital(db,hospital_data.hospital_id,hospital_data.hospital_name,hospital_data.county,current_user=current_user)
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
@router.get("/{hospital_id}",response_model=HospitalResponse)
def read_hospital(hospital_id:str,db:Session=Depends(get_db)):
    hospital=get_hospital_by_id(db,hospital_id)
    if not hospital:
        raise HTTPException(404,detail="Hospital not found")
    return hospital
@router.get("/",response_model=list[HospitalResponse])
def read_all_hospitals(db:Session=Depends(get_db)):
    return get_all_hospitals(db)
