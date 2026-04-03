from fastapi import APIRouter,Depends,HTTPException,Request
from schemas.transfer import TransferRequest,TransferResponse
from sqlalchemy.orm import Session
from models.user import User
from core.dependencies import get_user_object
from core.permissions import require_roles
from core.db import get_db
from models.transfer import Transfer
from services.transfer import transfer_patient
router=APIRouter(prefix="/transfers",tags=["Transfers"])
@router.post("/{admission_id}/transfer",response_model=TransferResponse)
def transfer(admission_id:str,request:TransferRequest,http_request:Request,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    try:
        transfer= transfer_patient(db,admission_id,request.new_bed_id,request.reason,current_user,http_request.client.host)
        return transfer
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
@router.get("/transfers",response_model=list[TransferResponse])
def get_transfers(db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR"))):
    return db.query(Transfer).all()

    