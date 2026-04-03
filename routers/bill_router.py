from fastapi import APIRouter,Depends,Query,Request
from sqlalchemy.orm import Session
from datetime import datetime
from core.db import get_db
from core.permissions import require_roles
from typing import List
from models.user import User
from core.dependencies import get_user_object
from schemas.bill import BillCreate,BillPayment,BillResponse
from services.bill import create_bill,get_all_bills,get_bill
router=APIRouter(prefix="/bills",tags=["Bills"])
@router.post("/bills",response_model=BillResponse)
def create_bill_route(visit_id:str=Query(...,description="Visit ID"),bill_data:BillCreate=...,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    bill_data.hospital_id=current_user.hospital_id
    bill=create_bill(db,visit_id,bill_data,current_user)
    return bill
@router.get("/bills",response_model=List[BillResponse])
def get_bills_route(start_date:datetime=Query(None),end_date:datetime=Query(None),db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    bills=get_all_bills(db,current_user,start_date,end_date)
    return bills
@router.get("/{bill_id}",response_model=BillResponse)
def get_bill_route(bill_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    bill=get_bill(db,bill_id,current_user)
    return bill
