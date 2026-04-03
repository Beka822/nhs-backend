from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from core.dependencies import get_user_object
from schemas.bill_item import BillItemCreate,BillItemResponse
from models.user import User
from core.db import get_db
from services.bill_item import add_bill_item,get_bill_item
router=APIRouter(prefix="/bills",tags=["Bills"])
@router.post("/{bill_id}/items",response_model=BillItemResponse)
def create_bill_item(bill_id:str,data:BillItemCreate,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return add_bill_item(bill_id=bill_id,data=data,db=db,current_user=current_user)
@router.get("/{bill_id}/items",response_model=list[BillItemResponse])
def get_bill_item_route(bill_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    items=get_bill_item(db,bill_id,current_user)
    return items