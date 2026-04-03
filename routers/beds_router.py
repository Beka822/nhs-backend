from fastapi import APIRouter,Depends,Request,HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_user_object
from schemas.bed import BedCreateRequest,BedResponse
from models.user import User
from core.db import get_db
from core.permissions import require_roles
from services.bed import create_bed,get_beds,update_bed,delete_bed
router=APIRouter(prefix="/beds",tags=["Beds"])
@router.post("/",response_model=BedResponse)
def create_bed_endpoint(request:BedCreateRequest,http_request:Request,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR"))):
    try:
        bed=create_bed(db=db,bed_data=request,current_user=current_user,ip_address=http_request.client.host)
        return bed
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
@router.get("/",response_model=list[BedResponse])
def list_beds_endpoint(ward_id:str|None=None,db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_:dict=Depends(require_roles("ADMIN","DOCTOR"))):
    beds=get_beds(db=db,ward_id=ward_id,current_user=current_user)
    return beds
@router.put("/{bed_id}",response_model=BedResponse)
def update_bed_endpoint(bed_id:str,update_data:dict,http_request:Request,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR"))):
    try:
        bed=update_bed(db=db,bed_id=bed_id,update_data=update_data,current_user=current_user,ip_address=http_request.client.host)
        return bed
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
@router.delete("/{bed_id}")
def delete_bed_endpoint(bed_id:str,http_request:Request,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR"))):
    try:
        result=delete_bed(db=db,bed_id=bed_id,current_user=current_user,ip_address=http_request.client.host)
        return result
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
