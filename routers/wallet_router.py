from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
import time
from typing import Optional
from models.user import User
from core.db import get_db
from services.wallet import (get_wallet_by_patient,get_wallet_transactions,initiate_stk_push)
from schemas.wallet import WalletResponse,WalletTransactionResponse,WalletTopUpRequest
from core.dependencies import get_user_object
router=APIRouter(prefix="/wallet",tags=["Wallet"])
@router.get("/balance/{patient_id}",response_model=Optional[WalletResponse])
def get_balance(patient_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    wallet=get_wallet_by_patient(db,patient_id)
    return wallet
@router.get("/transactions/{patient_id}",response_model=list[WalletTransactionResponse])
def transactions(patient_id:str,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    return get_wallet_transactions(db,patient_id)
@router.post("/topup")
def topup(
    request:WalletTopUpRequest,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_user_object)
):
    response=initiate_stk_push(db=db,Phone_number=request.phone_number,amount=request.amount,reference=request.reference)
    return response