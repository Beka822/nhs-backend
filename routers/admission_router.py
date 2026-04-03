from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.db import get_db
from core.permissions import require_roles
from core.dependencies import get_user_object
from schemas.admission import AdmissionCreate,AdmissionResponse
from models.admission import Admission
from models.user import User
from services.admission import create_admission,discharge_patient,get_active_admissions
router=APIRouter(prefix="/admissions",tags=["Admissions"])
@router.post("/{visit_id}",response_model=AdmissionResponse)
async def admit_patient(data:AdmissionCreate,visit_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR"))):
    return await create_admission(data=data,db=db,current_user=current_user,visit_id=visit_id)
@router.get("/active",response_model=list[AdmissionResponse])
def active_admission(db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    return get_active_admissions(db,User.hospital_id,current_user)
@router.get("/{admission_id}",response_model=AdmissionResponse)
def get_admission(admission_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    admission=db.query(Admission).filter(Admission.admission_id==admission_id,Admission.hospital_id==current_user.hospital_id).first()
    if not admission:
        raise HTTPException(404,detail="Admission not found")
    return admission
@router.post("/{admission_id}/discharge",response_model=AdmissionResponse)
async def discharge(admission_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR"))):
    return await discharge_patient(db=db,admission_id=admission_id,current_user=current_user)
