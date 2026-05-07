from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from models.user import User
from core.db import get_db
from core.dependencies import get_user_object
from services.pharmacy import dispense_drug,pharmacy_sales_summary,top_selling_drugs,low_stock_drugs
from schemas.pharmacysale import PharmacySaleCreate
router=APIRouter(prefix="/pharmacy-sales",tags=["Pharmacy Sales"])
@router.post("/")
def dispense(data:PharmacySaleCreate,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return dispense_drug(db,current_user,data)
@router.get("/summary")
def summary(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return pharmacy_sales_summary(db,current_user)
@router.get("/top-selling")
def top_selling(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return top_selling_drugs(db,current_user)
@router.get("/low-stock")
def low_stock(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return low_stock_drugs(db,current_user)