from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from models.user import User
from core.dependencies import get_user_object,get_current_user
from core.permissions import require_roles
from schemas.user import UserCreate,UserResponse
from services.user import create_user,get_user_by_id,get_all_users
router=APIRouter(prefix="/users",tags=["Users"])
@router.post("/",response_model=UserResponse)
def register_user(user_data:UserCreate,db:Session=Depends(get_db)):
    try:
        user=create_user(db=db,user_id=user_data.user_id,full_name=user_data.full_name,hospital_id=user_data.hospital_id,role=user_data.role,password=user_data.password)
        return user
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
@router.get("/users/me")
def get_me(current_user:User=Depends(get_user_object)):
    return{
        "user_id":current_user.user_id,
        "role":current_user.role,
        "hospital_id":current_user.hospital_id,
    }
@router.get("/{user_id}",response_model=UserResponse)
def read_user(user_id:str,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR"))):
    user=get_user_by_id(db,user_id,current_user)
    if not user:
        raise HTTPException(404,detail="User not found")
    return user
@router.get("/",response_model=list[UserResponse])
def read_all_users(db:Session=Depends(get_db),current_user:User=Depends(get_user_object),_=Depends(require_roles("ADMIN","DOCTOR","SUPER_ADMIN"))):
    return get_all_users(db,current_user)

