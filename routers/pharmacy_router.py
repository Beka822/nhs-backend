from fastapi import APIRouter,Depends
from schemas.pharmacy import DrugCreate,DrugResponse,DrugUpdate
from core.db import get_db
from services.pharmacy import create_drug,update_drug,get_drugs,near_expiry_drugs,expired_drugs,expiring_inventory_value
from models.user import User
from core.dependencies import get_user_object
from sqlalchemy.orm import Session
router=APIRouter(prefix="/drugs",tags=["Drugs"])
@router.post("/")
def create(data:DrugCreate,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return create_drug(db,current_user,data)
@router.put("/{drug_id}")
def update(drug_id:int,data:DrugUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return update_drug(db,drug_id,current_user,data)
@router.get("/")
def get_all(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return get_drugs(db,current_user)
@router.get("/near-expiry")
def near_expiry(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return near_expiry_drugs(db,current_user)
@router.get("/expired")
def expired(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return expired_drugs(db,current_user)
@router.get("/expiring-value")
def expiring_value(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return expiring_inventory_value(db,current_user)