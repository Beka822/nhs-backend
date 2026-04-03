from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.visit_addendum import (VisitAddendumCreate,VisitAddendumResponse)
from services.visit_addendum import (create_visit_addendum,get_visit_addendum_for_patient,get_all_visit_addenda_by_patient)
from core.permissions import require_roles
router=APIRouter(prefix="/visit-addenda",tags=["Visit Addenda"])
@router.post("/",response_model=VisitAddendumResponse)
def register_visit_addendum(addendum_data:VisitAddendumCreate,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    return create_visit_addendum(db,addendum_data,current_user)
@router.get("/{patient_id}/{visit_id}",response_model=list[VisitAddendumResponse])
def read_visit_addendum(patient_id:str,visit_id:str,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    return get_visit_addendum_for_patient(db,patient_id,visit_id)
@router.get("/{patient_id}",response_model=list[VisitAddendumResponse])
def read_all_visit_addenda(patient_id:str,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    return get_all_visit_addenda_by_patient(db,patient_id)
