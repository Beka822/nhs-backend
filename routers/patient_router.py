from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.patient import PatientCreate,PatientResponse,PatientPagResponse
from services.patient import (create_patient,get_patient_by_id,get_all_patients)
from core.permissions import require_roles
router=APIRouter(prefix="/patients",tags=["Patients"])
@router.post("/",response_model=PatientResponse)
def register_patient(patient_data:PatientCreate,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    try:
        return create_patient(db,patient_data,current_user)
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
@router.get("/{patient_id}",response_model=PatientResponse)
def read_patient(patient_id:str,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    patient=get_patient_by_id(db,patient_id,current_user)
    if not patient:
        raise HTTPException(404,detail="Patient not found")
    return patient
@router.get("/",response_model=PatientPagResponse)
def read_all_patients(page:int=Query(1,ge=1),page_size:int=Query(10,ge=1,le=100),db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    return get_all_patients(db,current_user,page,page_size)
