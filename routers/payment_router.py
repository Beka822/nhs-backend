from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from schemas.payment import PaymentCreate,PaymentResponse
from models.user import User
from core.dependencies import get_user_object
from services.payment import create_payment,get_payments
from core.db import get_db
from core.permissions import require_roles
router=APIRouter(prefix="/payments",tags=["Payments"])
@router.post("/bill/{bill_id}/payments",response_model=PaymentResponse)
def add_payment(bill_id:str,payment:PaymentCreate,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN"))):
    return create_payment(db,payment,bill_id,current_user)
@router.get("/",response_model=list[PaymentResponse])
def get_payments_route(bill_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return get_payments(db,bill_id,current_user)
