from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from models.visit import Visit
from models.user import User
from core.dependencies import get_user_object
from core.db import get_db
from schemas.visit import VisitCreate,VisitResponse,ResponseModel,VisitUpdate
from services.visit import (create_visit,get_visit_by_id,get_all_visits_for_patient)
from core.permissions import require_roles
router=APIRouter(prefix="/visits",tags=["Visits"])
@router.post("/",response_model=ResponseModel)
def register_visit(data:VisitCreate,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE","STAFF"))):
    try:
        return create_visit(db,data,current_user)
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
@router.get("/{patient_id}/{visit_id}",response_model=VisitResponse)
def read_visit(patient_id:str,visit_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE","STAFF"))):
    visit=get_visit_by_id(db,patient_id,visit_id,current_user)
    db.refresh(visit)
    if not visit:
        raise HTTPException(404,detail="Visit not found")
    return visit
@router.get("/{patient_id}",response_model=list[VisitResponse])
def read_all_visits(patient_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE","STAFF"))):
    return get_all_visits_for_patient(db,patient_id,current_user)
@router.put("/{visit_id}")
def update_visit(
    visit_id:str,
    data:VisitUpdate,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_user_object)
):
    visit=db.query(Visit).filter(Visit.visit_id==visit_id,Visit.hospital_id==current_user.hospital_id).first()
    if not visit:
        raise ValueError("Visit not found")
    visit.symptoms=data.symptoms
    visit.diagnosis=data.diagnosis
    visit.treatment=data.treatment
    visit.notes=data.notes
    visit.status="COMPLETED"
    db.commit()
    db.refresh(visit)
    return visit

