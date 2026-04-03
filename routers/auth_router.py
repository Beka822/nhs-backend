from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from schemas.auth import LoginRequest
from jose import jwt,JWTError
from core.security import SECRET_KEY,ALGORITHM
from core.db import get_db
from models.user import User
from core.security import verify_password,create_access_token,create_refresh_token
router=APIRouter(prefix="/auth",tags=["Authentication"])
@router.post("/login")
def login(login_data:LoginRequest,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.user_id==login_data.user_id).first()
    if not user:
        raise HTTPException(401,detail="Invalid credentials")
    if not verify_password(login_data.password,user.hashed_password):
        raise HTTPException(401,detail="Invalid credentials")
    access_token=create_access_token(data={"sub":user.user_id,"role":user.role.value,"hospital_id":user.hospital_id})
    refresh_token=create_refresh_token({"sub":user.user_id})
    return {"access_token":access_token,"refresh_token":refresh_token,"token_type":"bearer","hospital_id":user.hospital_id,"role":user.role}
@router.post("/refresh")
def refresh_token(refresh_token:str):
    try:
        payload=jwt.decode(refresh_token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=payload.get("sub")
        new_access_token=create_access_token({"sub":user_id})
        return {"access_token":new_access_token}
    except JWTError:
        raise HTTPException(401,detail="Invalid refresh token")
    