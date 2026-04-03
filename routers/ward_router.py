from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session
from models.user import User
from core.dependencies import get_user_object
from schemas.ward import WardCreate,WardUpdate,WardResponse
from services.ward import create_ward,get_wards,delete_ward,update_ward
from core.permissions import require_roles
from core.db import get_db
router=APIRouter(prefix="/wards",tags=["Wards"])
@router.post("/",response_model=WardResponse)
def create(request:WardCreate,http_request:Request,db:Session=Depends(get_db),_:dict=Depends(require_roles("ADMIN")),current_user:User=Depends(get_user_object)):
    return create_ward(db,request,current_user)
@router.get("/",response_model=list[WardResponse])
def list_wards(hospital_id:str,db:Session=Depends(get_db),_:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE")),current_user:User=Depends(get_user_object)):
    hospital_id=current_user.hospital_id
    return get_wards(db,hospital_id,current_user)
@router.put("/{ward_id}",response_model=WardResponse)
def update(ward_id:str,request:WardUpdate,http_request:Request,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN"))):
    return update_ward(db,ward_id,request,current_user,http_request.client.host)
@router.delete("/{ward_id}")
def delete(ward_id:str,http_request:Request,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN"))):
    return delete_ward(db,ward_id,current_user,http_request.client.host)

